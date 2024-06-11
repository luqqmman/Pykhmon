from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView, DeleteView, View
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.conf import settings
from django.db.models import Sum

from nanoid import generate
from string import ascii_letters, ascii_lowercase


from .mikrotik.routeros_api import HotspotApi
from .mikrotik.wifiqr import generate_qr, create_voucher_pdf

from .mixins import SessionRequiredMixin
from .models import Session, Profile, Voucher, VoucherPdf
from .forms import ProfileForm, VoucherForm

from reportlab.pdfgen import canvas
from PIL import Image
from datetime import date, timedelta
import os



class CreateSession(CreateView):
    model = Session
    fields = '__all__'
    template_name = 'dashboard/create_session.html'
    success_url = reverse_lazy('select_session')


class SelectSession(View):
    def get(self, request, *args, **kwargs):
        context = {
            'sessions': Session.objects.all()
        }
        return render(request, 'dashboard/select_session.html', context)
    
    def post(self, request, *args, **kwargs):
        if "session_name" in request.POST:
            session = Session.objects.filter(session_name=request.POST["session_name"]).first()
            request.session["pk"] = session.pk
            request.session["api"] = HotspotApi(session.mikrotik_IP, session.username, session.password, session.hotspot_server_name).to_dict()
            return redirect(reverse('dashboard'))
        messages.warning(request, "You don't have any session")
        return redirect(reverse('select_session'))


class Dashboard(SessionRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        hotspot = HotspotApi.from_dict(request.session['api'])
        resource = hotspot.resource()
        if resource:
            resource = [(key.replace('-', '_'), val) for key, val in resource.items()]
            context = {
                'resource': dict(resource),
                'active_users': hotspot.get_active_users(),
            }
            context.update(resource)
            return render(request, 'dashboard/dashboard.html', context)
        messages.warning(request, "Connection error: Router address unreachable")
        return render(request, 'dashboard/dashboard.html')


class CreateProfile(SessionRequiredMixin, CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'dashboard/create_profile.html'
    success_url = reverse_lazy('list_profile')
    

    def form_valid(self, form):
        form.instance.session = Session.objects.get(pk=self.request.session["pk"])
        profile = form.save()
        hotspot = HotspotApi.from_dict(self.request.session['api'])
        hotspot.add_profile(profile.profile_name, profile.shared_users, profile.rate_limit())
        return super().form_valid(form)


class ListProfile(SessionRequiredMixin, ListView):
    model = Profile
    template_name = 'dashboard/list_profile.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        session = self.request.session["pk"]
        return Profile.objects.filter(session=session)


class ListVoucher(SessionRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        session = self.request.session["pk"]
        vouchers = Voucher.objects.filter(session=session)

        hotspot = HotspotApi.from_dict(self.request.session['api'])
        active_users = hotspot.get_active_users()
        users = hotspot.get_users()

        v_list = []
        for user in users:
            user = dict([(key.replace('-', '_'), val) for key, val in user.items()])
            voucher = vouchers.filter(username=user['name'])
            if voucher.count() < 1: 
                continue

            # voucher = voucher.first()
            v = voucher.first().serialize()
            v.update(user)
            v.update({'current_price': voucher.first().get_price(len(active_users))})
            v_list.append(v)

            if user['uptime'] == '0s' or voucher.first().checkout_date: 
                continue
            voucher.update(checkout_date=date.today())

        print(v_list[-1])
        print(len(active_users))
        context = {
            'vouchers': v_list
        }

        return render(request, 'dashboard/list_voucher.html', context)
        # if users:
        #     for user in users:
        #         if user['uptime'] == '0s': continue
        #         voucher = vouchers.filter(username=user['name'])
        #         if voucher.count(): voucher.update(checkout_date=date.today())
        # else:
        #     messages.warning(self.request, "Connection error: Router address unreachable")
        # return context

    


# View untuk membuat voucher dan PDF
class CreateVoucher(SessionRequiredMixin, FormView):
    form_class = VoucherForm
    template_name = 'dashboard/create_voucher.html'
    success_url = reverse_lazy('list_voucher')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        price = form.cleaned_data['price']
        qty = form.cleaned_data['qty']
        uptime_value = form.cleaned_data['uptime_value']
        uptime_unit = form.cleaned_data['uptime_unit']
        uptime_limit = f"{uptime_value}{uptime_unit}"

        profile = Profile.objects.get(profile_name=form.cleaned_data['profile'])
        session = Session.objects.get(pk=self.request.session["pk"])
        hotspot = HotspotApi.from_dict(self.request.session['api'])
        
        vouchers = []
        for _ in range(int(qty)):
            username = generate(ascii_lowercase, 8)
            password = generate(ascii_letters, 8)
            if hotspot.add_user(username, password, uptime_limit, profile.profile_name):
                voucher = Voucher(username=username, password=password, price=price, session=session, profile=profile, uptime_value=uptime_value, uptime_unit=uptime_unit)
                voucher.save()
                vouchers.append(model_to_dict(voucher))
                qr_path = os.path.join(settings.QR_DIR, f"{username}.png")
                generate_qr(session.DNS_name, username, password, qr_path)
        
        VoucherPdf(session=session, name=name).save()
        pdf_path = os.path.join(settings.PDF_DIR, f"{name}.pdf")
        create_voucher_pdf(vouchers, settings.QR_DIR, pdf_path)
        
        return super().form_valid(form)


class ListVoucherPdf(SessionRequiredMixin, ListView):
    model = VoucherPdf
    template_name = 'dashboard/list_voucher_pdf.html'
    context_object_name = 'voucher_pdf'

    def get_queryset(self):
        session = self.request.session["pk"]
        return VoucherPdf.objects.filter(session=session)


class DetailVoucherPdf(SessionRequiredMixin, DetailView):
    model = VoucherPdf
    template_name = 'dashboard/detail_voucher_pdf.html'
    context_object_name = 'pdf'


class Income(SessionRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        session = Session.objects.get(pk=self.request.session["pk"])
        vouchers = Voucher.objects.filter(session=session)
        daily = vouchers.filter(checkout_date=date.today()).aggregate(Sum('price_min', default=0))
        weekly = vouchers.filter(checkout_date__gte=date.today()-timedelta(days=7)).aggregate(Sum('price_min', default=0))
        monthly = vouchers.filter(checkout_date__gte=date.today()-timedelta(weeks=4)).aggregate(Sum('price_min', default=0))
        context = {
            'daily': daily,
            'weekly': weekly,
            'monthly': monthly
        }
        return render(self.request, 'dashboard/income.html', context)



