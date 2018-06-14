# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'login/', views.Login.as_view(), name='login'),
    url(r'register/', views.SignUpAPIView.as_view(), name='register'),
]
