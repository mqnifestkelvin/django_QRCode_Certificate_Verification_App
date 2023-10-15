from django import forms
from .models import Certificate


class VerifyForm(forms.ModelForm):
    encrypted_byte_code = forms.CharField()

    class Meta:
        model = Certificate
        fields = ['encrypted_byte_code']


class EmailForm(forms.Form):
    email = forms.EmailField(label="Email Address")

class OTPForm(forms.Form):
   otp = forms.CharField(label="Enter OTP", widget=forms.PasswordInput(attrs={'maxlength': '6'}))
