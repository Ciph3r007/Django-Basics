from django.contrib import admin
from django.db.models.aggregates import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models

# Register your models here.
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders_count']
    ordering = ['first_name', 'last_name']
    list_editable = ['membership']
    list_per_page = 20

    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        url = reverse('admin:store_order_changelist')\
            + '?' + urlencode({
                'customer__id': str(customer.id)
            })
        
        return format_html(f'<a href={url}>{customer.orders_count}</a>')
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_name']
    list_editable = ['unit_price']
    list_per_page = 20
    # Displaying 'collection' directly is much better. Needed only when retrieving unavailable fields
    list_select_related = ['collection'] 

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'
    
    # Displaying 'collection' directly is much better. Needed only when retrieving unavailable fields
    @admin.display(ordering='collection')
    def collection_name(self, product):
        return product.collection.title

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'payment_status', 'customer']
    ordering = ['-placed_at']
    list_per_page = 20

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = reverse('admin:store_product_changelist')\
            + '?' + urlencode({
                'collection__id': str(collection.id)
            })

        return format_html(f'<a href="{url}">{collection.products_count}</a>')
    
    # overrides base query
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )

