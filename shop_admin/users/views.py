from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Country
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
# Import các thư viện phục vụ gửi email
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


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
    return render(request,'register.html',{'form':form})

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
    return render(request,'login.html',{'form':form})

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


    return render(request, 'account.html',{'countries':countries})


