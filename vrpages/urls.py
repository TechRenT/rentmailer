from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^vrpages_list/$', views.vrpages_list, name='vrpages_list'),
    url(r'^(?P<pk>\d+)/$', views.vrpage_detail, name='vrpage_detail'),
    url(r'^create/$', views.VRPageCreateView.as_view(), name='create_vrpage'),
    url(r'^edit/(?P<pk>\d+)/$', views.VRPageUpdateView.as_view(), name='update_vrpage'),
    url(r'^delete/(?P<pk>\d+)/$', views.VRPageDeleteView.as_view(), name='delete_vrpage'),
    url(r'^templates_list/$', views.templates_list, name='templates_list'),
    url(r'^template/(?P<pk>\d+)/$', views.template_detail, name='template_detail'),
    url(r'^create_template/$', views.MessageTemplateCreateView.as_view(), name='create_template'),
    url(r'^edit_template/(?P<pk>\d+)/$', views.MessageTemplateUpdateView.as_view(), name='edit_template'),
    url(r'^delete_template/(?P<pk>\d+)/$', views.MessageTemplateDeleteView.as_view(), name='delete_template'),
    url(r'^messages/$', views.messages_list, name='messages_list'),
    url(r'^messages/(?P<pk>\d+)/no_email/$', views.no_email, name='no_email'),
    url(r'^messages/(?P<pk>\d+)/(?P<template_type>\w+)/$', views.send_email, name='send_email'),
    url(r'^unsubscribes_list/$', views.unsubscribes_list, name='unsubscribes_list'),
    url(r'^create_unsubscribe_from_vrpage/$', views.unsubscribe_from_vrpage, name='unsubscribe_from_vrpage'),
    url(r'^create_unsubscribe_permanently/$', views.unsubscribe_permanently, name='unsubscribe_permanently'),
    url(r'^create_unsubscribe_entire_domain/$', views.unsubscribe_entire_domain, name='unsubscribe_entire_domain'),
]