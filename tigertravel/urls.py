from django.urls import path
from .views import RequestCreateView, RequestListView, GroupListView, GroupDetailView
from . import views
from uniauth.decorators import login_required
from users import views as user_views

urlpatterns = [
    path('', login_required(RequestCreateView.as_view()), name='tigertravel-home'),
    path('listings/', login_required(RequestListView.as_view()), name='tigertravel-listings'),
    path('groups/', login_required(GroupListView.as_view()), name='tigertravel-groups'),
    path('groups/<int:pk>', login_required(GroupDetailView.as_view()), name='group-detail'),
    path('profile/', user_views.profile, name='tigertravel-profile'),

]