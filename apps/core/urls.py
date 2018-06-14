# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import url


def generate_url(regex, view, name=None):
    regex = r'^' + settings.API_VERSION_URL + regex
    return url(regex, view, name=name)


urlpatterns = [
]
