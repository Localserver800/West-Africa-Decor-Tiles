from django.contrib import admin
from .models import Product, Stock, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'is_primary']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'price', 'current_stock']
    list_filter = ['name']
    search_fields = ['name', 'sku']
    inlines = [ProductImageInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(Stock)
admin.site.register(ProductImage)