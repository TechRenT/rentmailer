from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^messages/$', views.messages_list, name='messages_list'),
    url(r'^messages/(?P<pk>\d+)/$', views.send_email, name='send_email'),
]