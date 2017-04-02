from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^vrpages_list/$', views.vrpages_list, name='vrpages_list'),
    url(r'^messages/$', views.messages_list, name='messages_list'),
    url(r'^messages/(?P<pk>\d+)/no_email/$', views.no_email, name='no_email'),
    url(r'^messages/(?P<pk>\d+)/(?P<template_type>\w+)/$', views.send_email, name='send_email'),
]