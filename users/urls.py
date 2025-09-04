from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('wishlist/add-remove/<int:product_id>/', views.wishlist_add_remove, name='wishlist_add_remove'),
    path('wishlist/', views.wishlist_detail, name='wishlist_detail'),
]