from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class EmailLoginForm(forms.Form):
    email = forms.EmailField(label="البريد الإلكتروني")
    password = forms.CharField(widget=forms.PasswordInput, label="كلمة السر")

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if email and password:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("البريد الإلكتروني أو كلمة السر غير صحيحة")
            
            self.user = authenticate(username=user_obj.username, password=password)
            if not self.user:
                raise forms.ValidationError("البريد الإلكتروني أو كلمة السر غير صحيحة")
        return cleaned_data

    def get_user(self):
        return self.user

class CustomSignUp(UserCreationForm):
    email= forms.EmailField(required=True)
    class Meta:
        model= User
        fields= ['username', 'email', 'password1', 'password2']
        