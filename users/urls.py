from django.urls import path
from .views import CustomLoginView, VerifyCodeView
from . import views

urlpatterns = [
    path('whatsapp-login/', CustomLoginView.as_view(), name='whatsapp_login'),
    path('verify/', VerifyCodeView.as_view(), name='verify_code'),
    path('profile/', views.profile, name='profile'),
    path('wishlist/add-remove/<int:product_id>/', views.wishlist_add_remove, name='wishlist_add_remove'),
    path('wishlist/', views.wishlist_detail, name='wishlist_detail'),
]