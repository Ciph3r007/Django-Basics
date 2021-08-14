from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    ordering = ['first_name', 'last_name']
    list_editable = ['membership']
    list_per_page = 20

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

admin.site.register(models.Collection)
