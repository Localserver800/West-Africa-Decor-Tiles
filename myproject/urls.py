from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from myproject.views import home, admin_dashboard
from users.views import register

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('orders/', include('orders.urls')),
    path('inventory/', include('inventory.urls')),
    path('users/', include('users.urls')),
    path('', home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)