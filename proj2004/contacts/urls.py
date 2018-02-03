from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('list/class/<clazz>/', views.clazz_list, name='clazz_list'),
    path('list/department/<department>/', views.department_list, name='department_list'),
    path('list/', views.department_list, name='department_list'),
    path('<username>/', views.profile, name='profile'),
    path('<username>/edit/', views.profile_edit, name='profile_edit'),
]
