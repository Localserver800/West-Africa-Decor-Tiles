from django.urls import path
from . import views

urlpatterns = [
    path('catalog/', views.product_catalog, name='product_catalog'),
    path('low-stock-alert/', views.check_low_stock, name='check_low_stock'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/', views.product_management_list, name='product_management_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/update/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
]
