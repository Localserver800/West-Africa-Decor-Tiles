from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from orders.forms import CartAddProductForm
from django.contrib.auth.decorators import login_required
from communications.utils import simulate_email
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def product_list(request):
    """View to display all products with optional search and pagination"""
    products_list = Product.objects.all()
    categories = Category.objects.all()
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products_list = products_list.filter(category=category)

    # Simple search functionality
    # For better performance, consider adding a database index to the 'name' field.
    search_query = request.GET.get('search', '')
    if search_query:
        products_list = products_list.filter(name__icontains=search_query)

    # Price range filtering
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        products_list = products_list.filter(price__gte=min_price)
    if max_price:
        products_list = products_list.filter(price__lte=max_price)

    # Sorting
    sort_by = request.GET.get('sort_by')
    if sort_by == 'price_asc':
        products_list = products_list.order_by('price')
    elif sort_by == 'price_desc':
        products_list = products_list.order_by('-price')
    else:
        products_list = products_list.order_by('-id') # Default sort by newest

    paginator = Paginator(products_list, 12)  # Show 12 products per page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)
    
    context = {'products': products, 'search_query': search_query, 'categories': categories, 'min_price': min_price, 'max_price': max_price}
    return render(request, 'inventory/product_catalog.html', context)

# ADD THIS NEW VIEW
from .forms import ReviewForm
from .models import Product, ProductImage, Review

def product_detail(request, product_id):
    """View to display detailed information about a single product"""
    product = get_object_or_404(Product.objects.prefetch_related('images', 'reviews__user'), id=product_id)
    product_images = product.images.all()
    reviews = product.reviews.all()

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.product = product
            new_review.user = request.user
            new_review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        review_form = ReviewForm()
    
    # Get primary image or first image as main display
    primary_image = None
    for image in product_images:
        if image.is_primary:
            primary_image = image
            break
    if not primary_image and product_images:
        primary_image = product_images[0]
    
    context = {
        'product': product,
        'product_images': product_images,
        'primary_image': primary_image,
        'reviews': reviews,
        'review_form': review_form,
    }
    return render(request, 'inventory/product_detail.html', context)

@login_required
def check_low_stock(request):
    low_stock_products = Product.objects.filter(current_stock__lt=10)
    
    if request.method == 'POST' and low_stock_products.exists():
        # Send email alerts for all low stock products
        from users.models import CustomUser
        admins = CustomUser.objects.filter(role='admin', is_active=True)
        
        for admin in admins:
            if admin.email:
                subject = "LOW STOCK REPORT - Action Required"
                message = "The following products are low in stock:\n\n"
                
                for product in low_stock_products:
                    message += f"- {product.name}: {product.current_stock} left (SKU: {product.sku})\n"
                
                message += "\nPlease restock these items immediately."
                simulate_email(admin.email, subject, message)
        
        return render(request, 'inventory/stock_alert_sent.html')
    
    return render(request, 'inventory/check_low_stock.html', {
        'low_stock_products': low_stock_products
    })

def product_catalog(request):
    products_list = Product.objects.all()
    categories = Category.objects.all()
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products_list = products_list.filter(category=category)

    # Simple search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products_list = products_list.filter(name__icontains=search_query)

    # Price range filtering
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        products_list = products_list.filter(price__gte=min_price)
    if max_price:
        products_list = products_list.filter(price__lte=max_price)

    # Filter by brand
    brand_query = request.GET.get('brand')
    if brand_query:
        products_list = products_list.filter(brand__icontains=brand_query)

    # Filter by material
    material_query = request.GET.get('material')
    if material_query:
        products_list = products_list.filter(material__icontains=material_query)

    # Sorting
    sort_by = request.GET.get('sort_by')
    if sort_by == 'price_asc':
        products_list = products_list.order_by('price')
    elif sort_by == 'price_desc':
        products_list = products_list.order_by('-price')
    else:
        products_list = products_list.order_by('-id') # Default sort by newest

    paginator = Paginator(products_list, 12)  # Show 12 products per page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    # Get unique brands and materials for filter options
    brands = Product.objects.order_by().values_list('brand', flat=True).distinct().exclude(brand__isnull=True).exclude(brand__exact='')
    materials = Product.objects.order_by().values_list('material', flat=True).distinct().exclude(material__isnull=True).exclude(material__exact='')

    context = {
        'products': products,
        'search_query': search_query,
        'categories': categories,
        'min_price': min_price,
        'max_price': max_price,
        'brands': brands,
        'materials': materials,
        'selected_brand': brand_query,
        'selected_material': material_query,
    }
    return render(request, 'inventory/product_catalog.html', context)
