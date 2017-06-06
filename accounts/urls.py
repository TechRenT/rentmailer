from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'logout/$', views.LogoutView.as_view(), name='logout'),
]