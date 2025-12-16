from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='邮箱')
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, label='角色')
    phone = forms.CharField(max_length=15, required=False, label='手机号')
    first_name = forms.CharField(max_length=30, required=True, label='姓名')
    last_name = forms.CharField(max_length=30, required=False, label='名')

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "phone", "role", "password1", "password2")
        labels = {
            'username': '学号',
            'password1': '密码',
            'password2': '确认密码',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 添加更友好的错误消息
        for field_name, field in self.fields.items():
            field.error_messages.update({
                'required': f'请填写{field.label}',
                'invalid': f'{field.label}格式不正确',
            })

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('该学号已被注册，请使用其他学号')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已被注册，请使用其他邮箱')
        return email

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