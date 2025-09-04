from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import CustomUserCreationForm, CustomUserChangeForm, AddressForm
from django.contrib.auth.decorators import login_required
from inventory.models import Product
from .models import Wishlist, Address
from orders.models import Order
from django.urls import reverse

@login_required
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.role = 'customer'  # Automatically set role to customer
            user.save()
            login(request, user)
            return redirect('product_catalog')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    user_form = CustomUserChangeForm(instance=request.user)
    address_form = AddressForm()
    addresses = Address.objects.filter(user=request.user)
    orders = Order.objects.filter(customer=request.user).order_by('-created')

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            user_form = CustomUserChangeForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                return redirect('profile')
        elif 'add_address' in request.POST:
            address_form = AddressForm(request.POST)
            if address_form.is_valid():
                new_address = address_form.save(commit=False)
                new_address.user = request.user
                new_address.save()
                return redirect('profile')
        elif 'delete_address' in request.POST:
            address_id = request.POST.get('address_id')
            address_to_delete = get_object_or_404(Address, id=address_id, user=request.user)
            address_to_delete.delete()
            return redirect('profile')

    context = {
        'user_form': user_form,
        'address_form': address_form,
        'addresses': addresses,
        'orders': orders,
    }
    return render(request, 'users/profile.html', context)

@login_required
def wishlist_add_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    if product in wishlist.products.all():
        wishlist.products.remove(product)
    else:
        wishlist.products.add(product)
    
    referer_url = request.META.get('HTTP_REFERER')
    if referer_url:
        return redirect(referer_url)
    else:
        return redirect(reverse('product_detail', kwargs={'product_id': product_id}))

@login_required
def wishlist_detail(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'users/wishlist_detail.html', {'wishlist': wishlist})
