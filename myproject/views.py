from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from inventory.models import Product, FlashSale
from orders.models import Order, OrderItem
from users.models import CustomUser
from django.db.models import Sum
from django.utils import timezone

def home(request):
    # Flash sales
    now = timezone.now()
    flash_sales = FlashSale.objects.filter(end_date__gt=now)
    flash_sale_products = [fs.product for fs in flash_sales]

    # Top selling products based on sales data
    top_selling_products = Product.objects.annotate(
        total_quantity_sold=Sum('orderitem__quantity')
    ).order_by('-total_quantity_sold').filter(total_quantity_sold__gt=0)[:4]

    # Premium products
    premium_products = Product.objects.filter(is_premium=True)[:4]

    # Carousel products - latest 3 products with images
    carousel_products = Product.objects.filter(image__isnull=False).order_by('-id')[:3]

    context = {
        'flash_sales': flash_sales,
        'flash_sale_products': flash_sale_products,
        'top_selling_products': top_selling_products,
        'premium_products': premium_products,
        'carousel_products': carousel_products,
    }
    return render(request, 'home.html', context)

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('/')
    
    # Fetch data for dashboard
    recent_orders = Order.objects.all().order_by('-created')[:5]
    low_stock_products = Product.objects.filter(current_stock__lt=10)
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_users = CustomUser.objects.count()

    context = {
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_users': total_users,
    }
    return render(request, 'admin_dashboard.html', context)
