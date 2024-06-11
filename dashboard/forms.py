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
    price = forms.IntegerField(min_value=1 ,label='Price')
    profile = forms.ModelChoiceField(queryset=Profile.objects.all(), widget=forms.Select, required=True)
    uptime_value = forms.IntegerField(min_value=1)
    uptime_unit = forms.ChoiceField(choices=UPTIME_UNIT_CHOICES)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'profile_name': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'download_limit_value': forms.NumberInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'download_limit_unit': forms.Select(attrs={'class': 'form-select mt-1 block w-full'}),
            'upload_limit_value': forms.NumberInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'upload_limit_unit': forms.Select(attrs={'class': 'form-select mt-1 block w-full'}),
            'shared_users': forms.NumberInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea mt-1 block w-full'}),
        }
