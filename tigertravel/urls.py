from django.urls import path
from .views import RequestCreateView, RequestListView
from . import views

urlpatterns = [
    path('', RequestCreateView.as_view(), name='tigertravel-home'),
    path('about/', RequestListView.as_view(), name='tigertravel-about'),
]