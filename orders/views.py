from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from inventory.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.http import HttpResponse
from .models import Order, OrderItem

from django.contrib import messages

@login_required
def checkout(request):
    cart = Cart(request)
    
    # Check stock before processing order
    for item in cart:
        if item['quantity'] > item['product'].current_stock:
            messages.error(request, f"Sorry, only {item['product'].current_stock} units of {item['product'].name} are available.")
            return redirect('cart_detail')
    
    if request.method == 'POST':
        # Create the order
        order = Order.objects.create(
            customer=request.user,
            total_amount=cart.get_total_price()
        )
        
        # Create order items from cart AND UPDATE INVENTORY
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )
            # DEDUCT STOCK FROM INVENTORY
            product = item['product']
            product.current_stock -= item['quantity']
            product.save()
        
        # Clear the cart after successful order
        cart.clear()
        
        # Simulate sending order confirmation email
        from communications.utils import simulate_email
        subject = f"Order Confirmation - Order #{order.id}"
        message = f"Dear {request.user.username},\n\nYour order #{order.id} has been placed successfully.\nTotal amount: GHS {order.total_amount}\n\nThank you for your purchase!"
        simulate_email(request.user.email, subject, message)
        
        # Handle payment method
        payment_method = request.POST.get('payment_method')
        if payment_method in ['cash', 'mobile_money']:
            order.paid = False # Mark as not paid yet for COD/Mobile Money
            order.status = 'Pending' # Set status to pending
            order.save()
            return redirect('order_confirmation', order_id=order.id)
        elif payment_method == 'stripe':
            # Redirect to payment view for Stripe processing
            return redirect('payment', order_id=order.id)
        
    return render(request, 'orders/checkout.html', {'cart': cart})

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_confirmation.html', {'order': order})

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'orders/cart_detail.html', {'cart': cart})

def create_order(request):
    return HttpResponse("Not implemented yet.")

def add_order_items(request, order_id):
    return HttpResponse("Not implemented yet.")

@login_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created')
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

from django.urls import reverse
from django.conf import settings
# import stripe # Comment out or remove stripe import

# stripe.api_key = settings.STRIPE_SECRET_KEY # Comment out or remove stripe.api_key

@login_required
def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    request.session['order_id'] = order.id # Add this line back
    
    # This is a dummy payment processor for school project
    # In a real application, you would integrate with a payment gateway like Stripe here.
    
    order.paid = True # Mark order as paid for demonstration
    order.status = 'Processing' # Update order status
    order.save()
    
    return redirect('payment_success') # Redirect to success page directly

@login_required
def payment_success(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    # order.paid = True # Already set in dummy payment
    # order.stripe_id = stripe_session_id # Comment out or remove
    order.save() # Save the order to persist changes
    del request.session['order_id']
    # del request.session['stripe_session_id'] # Comment out or remove
    return render(request, 'orders/payment_success.html')

@login_required
def payment_cancel(request):
    return render(request, 'orders/payment_cancel.html')

from .forms import OrderStatusUpdateForm

@login_required
def admin_order_list(request):
    if not request.user.is_staff:
        return redirect('/')
    orders = Order.objects.all().order_by('-created')
    
    for order in orders:
        order.status_form = OrderStatusUpdateForm(instance=order)

    return render(request, 'orders/admin_order_list.html', {'orders': orders})

@login_required
def admin_order_update_status(request, order_id):
    if not request.user.is_staff:
        return redirect('/')
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderStatusUpdateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('admin_order_list')
    return redirect('admin_order_list')