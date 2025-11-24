from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='邮箱')
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, label='角色')
    phone = forms.CharField(max_length=15, required=False, label='手机号')
    first_name = forms.CharField(max_length=30, required=True, label='姓')
    last_name = forms.CharField(max_length=30, required=True, label='名')

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "phone", "role", "password1", "password2")
        labels = {
            'username': '用户名',
            'password1': '密码',
            'password2': '确认密码',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.phone = self.cleaned_data["phone"]
        user.role = self.cleaned_data["role"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user