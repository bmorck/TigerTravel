from django.urls import path
from .views import RequestCreateView, RequestListView, GroupListView, GroupDetailView, RequestDeleteView
from . import views
from uniauth.decorators import login_required
from users import views as user_views

urlpatterns = [
    path('', views.login, name='tigertravel-login'),
    path('home/', login_required(RequestCreateView.as_view()), name='tigertravel-home'),
    path('profile/', login_required(RequestListView.as_view()), name='tigertravel-profile'),
    path('groups/', login_required(GroupListView.as_view()), name='tigertravel-groups'),
    path('groups/<int:pk>', login_required(GroupDetailView.as_view()), name='group-detail'),
    path('delete/<int:pk>', login_required(RequestDeleteView.as_view()), name='request-delete'),
    

]