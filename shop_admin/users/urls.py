from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='custom_logout'),
    path('update/', views.account_update, name='account_update'),
    
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<user_id>/<token>/', views.reset_password_confirm, name='password_reset_confirm'),
]