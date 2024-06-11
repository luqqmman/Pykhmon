from django import forms

from .models import Session, Profile, Voucher 

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['session']


class VoucherForm(forms.Form):
    UPTIME_UNIT_CHOICES = [
        ("s", "second"),
        ("m", "minute"),
        ("h", "hour"),
        ("d", "day"),
    ]

    name = forms.CharField(max_length=64)
    qty = forms.IntegerField(min_value=1 ,label='Quantity')
    price_min = forms.IntegerField(min_value=1)
    price_max = forms.IntegerField(min_value=1)
    profile = forms.ModelChoiceField(queryset=Profile.objects.all(), widget=forms.Select, required=True)
    uptime_value = forms.IntegerField(min_value=1)
    uptime_unit = forms.ChoiceField(choices=UPTIME_UNIT_CHOICES)
