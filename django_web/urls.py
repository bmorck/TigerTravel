from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tigertravel.urls')),
    path('accounts/', include('uniauth.urls.cas_only', namespace='uniauth')),
]
