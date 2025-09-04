from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    current_stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    material = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def is_low_stock(self):
        return self.current_stock < 10

    def get_discounted_price(self):
        if hasattr(self, 'flash_sales') and self.flash_sales.exists():
            flash_sale = self.flash_sales.first()
            if flash_sale.is_active():
                discount = self.price * (flash_sale.discount_percentage / 100)
                return round(self.price - discount, 2)
        return self.price

    def save(self, *args, **kwargs):
        if self.pk:
            original = Product.objects.get(pk=self.pk)
            if self.current_stock < 10 and original.current_stock >= 10:
                from communications.utils import simulate_email
                from users.models import CustomUser
                
                admins = CustomUser.objects.filter(role='admin', is_active=True)
                for admin in admins:
                    if admin.email:
                        subject = f"LOW STOCK ALERT: {self.name}"
                        message = f"""
                        Product: {self.name}
                        Current Stock: {self.current_stock}
                        SKU: {self.sku}
                        
                        Please restock immediately.
                        """
                        simulate_email(admin.email, subject, message)
        
        super().save(*args, **kwargs)

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    location = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'location')
        verbose_name_plural = "Stock"

    def __str__(self):
        return f"{self.product.name} - {self.location}: {self.quantity}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} Image"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.product.name}'

    class Meta:
        unique_together = ('product', 'user')
        ordering = ('-created_at',)

class FlashSale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='flash_sales')
    discount_percentage = models.PositiveIntegerField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.product.name} Flash Sale"

    def is_active(self):
        return self.end_date > timezone.now()