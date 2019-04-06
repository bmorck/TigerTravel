from django.urls import path
from .views import RequestCreateView, RequestListView, GroupListView
from . import views

urlpatterns = [
    path('', RequestCreateView.as_view(), name='tigertravel-home'),
    path('about/', RequestListView.as_view(), name='tigertravel-about'),
    path('groups/', GroupListView.as_view(), name='tigertravel-groups'),
]