from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.users.models import Users


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(max_length=255, required=True)

    class Meta:
        model = Users
        fields = ('username', 'password1', 'email')

class LoginUserForm(forms.Form):
    email = forms.EmailField(max_length=255, required=True)
    password = forms.CharField(max_length=20, required=True)


class PasswordResetForm(forms.Form):
    password1 = forms.CharField(max_length=255, required=True)
    password2 = forms.CharField(max_length=255, required=True)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2
