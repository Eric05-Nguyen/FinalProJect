from django.utils.http import urlsafe_base64_encode
from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Country
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
# Import các thư viện phục vụ gửi email
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

def register_view(request):
    if request.method=="POST":
        form=UserRegisterForm(request.POST,request.FILES)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])

            # Gán quyền người dùng
            user.is_superuser=False
            user.is_staff=False

            user.save()
            send_welcome_email(user)
            return HttpResponse("Đăng ký thành công,đã gửi email")
        
    else:
        form=UserRegisterForm()
    return render(request,'users/register.html',{'form':form})

# Xử lý login
def login_view(request):
    if request.method=='POST':
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)

            request.session['user_id']=user.id
            return redirect('index')
    else:
        form=AuthenticationForm()
    return render(request,'users/login.html',{'form':form})

def logout_view(request):
    logout(request)
    return redirect('login')



def send_welcome_email(user):
    subject='Chào mừng bạn đến với website'
    from_email=settings.DEFAULT_FROM_EMAIL
    to=[user.email]

    # Nội dung text fallback
    text_content= f"Chào {user.username}, cảm ơn bạn đã đăng ký."

    # render template
    html_content=render_to_string('emails/welcome_email.html',{'user':user})

    # Gửi email
    msg=EmailMultiAlternatives(subject,text_content,from_email,to)
    msg.attach_alternative(html_content,"text/html")
    msg.send()

@login_required(login_url='login') 
def account_update(request):
    countries = Country.objects.all()
    user=request.user
    if request.method=='POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        country_id = request.POST.get('id_country')
        avatar = request.FILES.get('avatar')
        password = request.POST.get('password')
        
        user.username=username
        user.email=email
        user.address=address
        user.phone=phone

        if avatar:
            user.avatar=avatar

        if country_id:
            country_obj=Country.objects.get(id=country_id)
            user.id_country=country_obj
        
        if password:
            user.set_password(password) 
        
        user.username=username
        user.email=email
        user.address=address
        user.phone=phone
        user.save()

        if password:
            update_session_auth_hash(request, user)
        messages.success(request, 'Cập nhật thành công')
        return redirect('account_update')


    return render(request, 'users/account.html',{'countries':countries})

# xử lý quên mật khẩu
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user_email=User.objects.filter(email=email).first()
        if user_email:
            # mã hóa id người dùng
            user_id= urlsafe_base64_encode(force_bytes(user_email.pk))
            # tạo token để bảo mật
            token=default_token_generator.make_token(user_email)
            domain=get_current_site(request).domain
            reset_link=f"http://{domain}/users/reset-password/{user_id}/{token}/"

            subject="Khôi phục mật khẩu"
            text_content = f"Chào bạn, click vào link sau để đổi mật khẩu: {reset_link}."
            msg=EmailMultiAlternatives(subject,text_content,settings.DEFAULT_FROM_EMAIL,[user_email.email])
            msg.send()
        messages.success(request, 'Đã gửi liên kết khôi phục mật khẩu')
    return render(request, 'users/forgot_password.html')       


# Xác thực token và lưu mk mới
def reset_password_confirm(request,user_id,token):
    try:
        uid=force_str(urlsafe_base64_decode(user_id))
        user=User.objects.get(pk=uid)
    except (User.DoesNotExist,ValueError,TypeError):
        user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        if request.method=='POST':
            new_password=request.POST.get('new_password')
            if new_password:
                user.set_password(new_password)
                user.save()
                messages.success(request,"Đã cập nhật mật khẩu thành công")
                return redirect('login')        
        return render(request, 'users/password_reset_confirm.html', {'validlink': True})
    else:
        return render(request, 'users/password_reset_confirm.html', {'validlink': False})