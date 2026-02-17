from django.urls import path, re_path
from django.views.generic import TemplateView
from django.conf import settings
import os

urlpatterns = [
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html'), name='index'),
]
