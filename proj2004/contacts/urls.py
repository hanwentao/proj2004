from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<username>/', views.profile, name='profile'),
    path('<username>/edit/', views.profile_edit, name='profile_edit'),
]
