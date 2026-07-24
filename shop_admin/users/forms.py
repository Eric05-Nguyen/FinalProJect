from django import forms
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(required=True, error_messages={'required': 'Vui lòng nhập địa chỉ email'})
    password=forms.CharField(widget=forms.PasswordInput,max_length=100)
    confirm_password=forms.CharField(widget=forms.PasswordInput,max_length=100)

    class Meta:
        model=CustomUser
        fields=['username','email','password','confirm_password','avatar','first_name','last_name','id_country']

        help_texts={
            'username':None,

        }

    def clean_username(self):
        username=self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Username đã tồn tại")
        return username
    
    def clean_email(self):
        email=self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Email đã tồn tại")
        return email
        
    def clean_avatar(self):
        avatar=self.cleaned_data.get('avatar')
        if avatar and avatar.size>1024*1024:
            raise ValidationError("Ảnh phải nhỏ hơn 1 MB")
        return avatar
        
    def clean(self):
        cleaned_data=super().clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Mật khẩu xác nhận không khớp")
        return cleaned_data

