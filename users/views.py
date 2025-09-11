from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, CustomUserChangeForm, AddressForm, VerificationCodeForm
from django.contrib.auth.decorators import login_required
from inventory.models import Product
from .models import Wishlist, Address, VerificationCode
from orders.models import Order
from django.urls import reverse
from django.views import View
from django.contrib.auth.views import LoginView
from django.conf import settings
from twilio.rest import Client
import random

class CustomLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        if user is not None:
            # Generate verification code
            code = str(random.randint(100000, 999999))
            VerificationCode.objects.create(user=user, code=code)

            # Send WhatsApp message
            try:
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                message = client.messages.create(
                    body=f'Your verification code is {code}',
                    from_=f'whatsapp:{settings.TWILIO_WHATSAPP_NUMBER}',
                    to=f'whatsapp:{user.phone_number}'
                )
                print(message.sid)
            except Exception as e:
                print(f"Error sending WhatsApp message: {e}")

            # Store user's pk in session to retrieve after verification
            self.request.session['user_pk_for_verification'] = user.pk
            return redirect('verify_code')

        return super().form_invalid(form)

class VerifyCodeView(View):
    def get(self, request):
        form = VerificationCodeForm()
        return render(request, 'users/verify_code.html', {'form': form})

    def post(self, request):
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            user_pk = request.session.get('user_pk_for_verification')
            if user_pk:
                try:
                    verification_code = VerificationCode.objects.get(user__pk=user_pk, code=code)
                    # Optional: Check if the code has expired
                    # if (timezone.now() - verification_code.created_at).seconds > 300: # 5 minutes
                    #     # Handle expired code
                    #     pass

                    user = verification_code.user
                    login(request, user)
                    verification_code.delete()
                    del request.session['user_pk_for_verification']
                    return redirect('product_catalog')
                except VerificationCode.DoesNotExist:
                    # Handle invalid code
                    pass
        return render(request, 'users/verify_code.html', {'form': form})

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