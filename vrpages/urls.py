from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^vrpages_list/$', views.vrpages_list, name='vrpages_list'),
    url(r'^(?P<pk>\d+)/$', views.vrpage_detail, name='vrpage_detail'),
    url(r'^create/$', views.VRPageCreateView.as_view(), name='create_vrpage'),
    url(r'^edit/(?P<pk>\d+)/$', views.VRPageUpdateView.as_view(), name='update_vrpage'),
    url(r'^delete/(?P<pk>\d+)/$', views.VRPageDeleteView.as_view(), name='delete_vrpage'),
    url(r'^messages/$', views.messages_list, name='messages_list'),
    url(r'^messages/(?P<pk>\d+)/no_email/$', views.no_email, name='no_email'),
    url(r'^messages/(?P<pk>\d+)/(?P<template_type>\w+)/$', views.send_email, name='send_email'),
]