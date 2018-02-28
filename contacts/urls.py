from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('class/<int:id_or_name>/', views.class_detail, name='class_detail'),
    path('class/<id_or_name>/', views.class_detail, name='class_detail'),
    # re_path(r'^department/(?P<id_or_code_or_name>[0-9]{3})/$', views.department_list, name='department_list'),
    # path('department/<int:id_or_code_or_name>/', views.department_list, name='department_list'),
    # path('department/<id_or_code_or_name>/', views.department_list, name='department_list'),
    path('overview/', views.overview, name='overview'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset_commit/', views.password_reset_commit, name='password_reset_commit'),
    path('password_reset_approve/', views.password_reset_approve, name='password_reset_approve'),
    re_path(r'^(?P<username>[0-9]{10})/$', views.profile, name='profile'),
    re_path(r'^(?P<username>[0-9]{10})/edit/$', views.profile_edit, name='profile_edit'),
]
