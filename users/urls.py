from django.urls import path
from django.contrib.auth.views import (
    LoginView, 
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView)

from . import views

# app_name = 'users'
urlpatterns = [
    path('register/', views.register, name='users-register'),
    path('profile/', views.profile, name='users-profile'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='users-login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='users-logout'),
    
    path('password-reset/', 
        PasswordResetView.as_view(template_name='users/password_reset.html'), 
        name='password_reset'),

    path('password-reset-done/', 
        PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), 
        name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', 
        PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), 
        name='password_reset_confirm'),
    
    path('pass-reset-complete',
        PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), 
        name='password_reset_complete'),
]