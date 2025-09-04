from django.urls import path
from . import views

urlpatterns = [
    path('catalog/', views.product_catalog, name='product_catalog'),
    path('low-stock-alert/', views.check_low_stock, name='check_low_stock'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
]