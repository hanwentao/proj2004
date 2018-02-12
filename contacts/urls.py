from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^(?P<username>[0-9]{10})/$', views.profile, name='profile'),
    re_path(r'^(?P<username>[0-9]{10})/edit/$', views.profile_edit, name='profile_edit'),
]
