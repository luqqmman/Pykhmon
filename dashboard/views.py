from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from nanoid import generate
from string import ascii_letters

from .mikrotik.routeros_api import HotspotApi
from .mikrotik.wifiqr import generate_qr

from .mixins import SessionRequiredMixin
from .models import Session, Profile, Voucher


class CreateSession(CreateView):
    model = Session
    fields = '__all__'
    template_name = 'dashboard/create_session.html'
    success_url = reverse_lazy('dashboard')


class SelectSession(View):
    def get(self, request, *args, **kwargs):
        context = {
            'sessions': Session.objects.all()
        }
        return render(request, 'dashboard/select_session.html', context)
    
    def post(self, request, *args, **kwargs):
        session_name = request.POST["session_name"]
        if session_name == "new_session":
            return redirect(reverse('create_session'))
        session = Session.objects.filter(session_name=session_name).first()
        request.session["hotspot_api"] = HotspotApi(session.mikrotik_IP, session.username, session.password, session.hotspot_server_name).to_dict()
        request.session["mikrotik"] = model_to_dict(session)
        return redirect(reverse('dashboard'))


class Dashboard(SessionRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        hotspot = HotspotApi.from_dict(request.session['hotspot_api'])
        context = {
            'resource': hotspot.resource()
        }
        return render(request, 'dashboard/dashboard.html', context)


class CreateVoucher(SessionRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/generate_voucher.html')

    def post(self, request, *args, **kwargs):
        hotspot = HotspotApi.from_dict(request.session['hotspot_api'])
        uptime = request.POST["uptime"]
        qty = request.POST["qty"]

        for _ in range(int(qty)):
            username = generate(ascii_letters, 8)
            password = generate(ascii_letters, 8)
            status = hotspot.add_user(username, password, uptime)
            if status:
                session = request.session["mikrotik"]
                generate_qr(session["DNS_name"], username, password, f"dashboard/static/dashboard/{username}.png")
        return redirect(reverse('test_voucher'))


def router_login(request):
    if request.method == "POST":
        router_address = request.POST["router_address"]
        username = request.POST["username"]
        password = request.POST["password"]
        server_name = request.POST["server_name"]

        request.session["hotspot"] = request.POST
        return redirect(reverse('dashboard'))
    return render(request, 'dashboard/router_login.html')


def dashboard(request):
    session = request.session["mikrotik"]
    hotspot = HotspotApi(hotspot["router_address"], hotspot["username"], hotspot["password"], hotspot["server_name"])

    context = {
        'resource': hotspot.resource()
    }
    return render(request, 'dashboard/dashboard.html', context)


def voucher(request):
    if request.method == "POST":
        hotspot = request.session["hotspot"]
        hotspot = HotspotApi(hotspot["router_address"], hotspot["username"], hotspot["password"], hotspot["server_name"])

        username = request.POST["username"]
        uptime = request.POST["uptime"]
        password = request.POST["password"]

        status = hotspot.add_user(username, password, uptime)
        if status:
            hotspot = request.session["hotspot"]
            generate_qr('10.10.10.2', username, password)
            return redirect(reverse('test_voucher'))
        return render(request, 'dashboard/voucher.html')
    return render(request, 'dashboard/voucher.html')


def test_voucher(request):
    return render(request, 'dashboard/test_voucher.html')