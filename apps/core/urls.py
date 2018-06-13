# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import url

from . import views


def generate_url(regex, view, name=None):
    regex = r'^' + settings.API_VERSION_URL + regex
    return url(regex, view, name=name)


urlpatterns = [
    url(r'contact-us/', views.SendContactUsEmailAPIView.as_view(), name='contact_us'),
]
