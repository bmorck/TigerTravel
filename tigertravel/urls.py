from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='tigertravel-home'),
    path('about/', views.about, name='tigertravel-about'),
]