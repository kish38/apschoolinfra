"""apschoolinfra URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from .views import *

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',home, name="home"),
    url(r'^logout/',logout_user),
    url(r'^register/',register_user),
    url(r'^register_success/',register_success),
    url(r'^teacher_login', teacher_login),
    url(r'^teacher', teacher_view),
    url(r'^add_device', add_device),
    url(r'^create_incident', create_incident),
    url(r'^technician_login', technician_login),
    url(r'^technician', technician_view),
    url(r'^admin_view', admin_view),

]
