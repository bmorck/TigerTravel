from django.urls import path
from .views import RequestCreateView, RequestListView, GroupListView
from . import views

urlpatterns = [
    path('', RequestCreateView.as_view(), name='tigertravel-home'),
    path('listings/', RequestListView.as_view(), name='tigertravel-listings'),
    path('groups/', GroupListView.as_view(), name='tigertravel-groups'),
]