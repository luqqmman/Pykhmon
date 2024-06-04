from django.contrib import admin

from .models import Session, Profile, Voucher

admin.site.register(Session)
admin.site.register(Profile)
admin.site.register(Voucher)