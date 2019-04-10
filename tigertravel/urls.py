from django.urls import path
from .views import RequestCreateView, RequestListView, GroupListView
from . import views
from uniauth.decorators import login_required

urlpatterns = [
    path('', login_required(RequestCreateView.as_view()), name='tigertravel-home'),
    path('listings/', RequestListView.as_view(), name='tigertravel-listings'),
    path('groups/', GroupListView.as_view(), name='tigertravel-groups'),
    path('profile/', GroupListView.as_view(), name='tigertravel-groups'),

]