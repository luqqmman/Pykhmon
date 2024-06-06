from django.contrib import admin

from .models import Session, Profile, Voucher, VoucherPdf

admin.site.register(Session)
admin.site.register(Profile)
admin.site.register(Voucher)
admin.site.register(VoucherPdf)