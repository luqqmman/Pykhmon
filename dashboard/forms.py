from django import forms

from .models import Session, Profile, Voucher 

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['session']


class VoucherForm(forms.ModelForm):
    profile = forms.ModelChoiceField(
        queryset=Profile.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select w-full px-4 py-2 rounded',
            'placeholder': 'Profile'
        })
    )
    qty = forms.IntegerField(
        label="Quantity",
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-input w-full px-4 py-2 rounded',
            'placeholder': 'Quantity'
        })
    )
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-input w-full px-4 py-2 rounded',
            'placeholder': 'Voucher Name'
        })
    )
    class Meta:
        model = Voucher
        fields = ['profile', 'uptime_value', 'uptime_unit', 'price_min', 'price_max']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input w-full px-4 py-2 rounded',
                'placeholder': 'Username'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-input w-full px-4 py-2 rounded',
                'placeholder': 'Password'
            }),
            'uptime_value': forms.NumberInput(attrs={
                'class': 'form-input w-full px-4 py-2 rounded',
                'placeholder': 'Uptime Value'
            }),
            'uptime_unit': forms.Select(attrs={
                'class': 'form-select w-full px-4 py-2 rounded'
            }),
            'price_min': forms.NumberInput(attrs={
                'class': 'form-input w-full px-4 py-2 rounded',
                'placeholder': 'Minimum Price'
            }),
            'price_max': forms.NumberInput(attrs={
                'class': 'form-input w-full px-4 py-2 rounded',
                'placeholder': 'Maximum Price'
            }),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = 'profile_name', 'download_limit_value', 'download_limit_unit', 'upload_limit_value', 'upload_limit_unit', 'shared_users', 'description'
        widgets = {
            'profile_name': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'download_limit_value': forms.NumberInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'download_limit_unit': forms.Select(attrs={'class': 'form-select mt-1 block w-full'}),
            'upload_limit_value': forms.NumberInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'upload_limit_unit': forms.Select(attrs={'class': 'form-select mt-1 block w-full'}),
            'shared_users': forms.NumberInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea mt-1 block w-full'}),
        }
