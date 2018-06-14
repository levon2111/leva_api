# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'login/', views.Login.as_view(), name='login'),
    url(r'confirm-account/', views.ConfirmAccountAPIView.as_view(), name='confirm_account'),
    url(r'forgot-password/', views.ForgotPasswordAPIView.as_view(), name='forgot_password'),
    url(r'register/', views.SignUpAPIView.as_view(), name='register'),
]
