from tags.models import TaggedItem
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models

class InventoryFilter(admin.SimpleListFilter):
    title='inventory' # Shown as 'By inventory'
    parameter_name = 'inventory' # Shown in the api link 

    def lookups(self, request, model_admin):
        filters = [
            ('<10', 'Low'),
            ('>=10', 'OK')
        ]
        return filters
    
    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        if self.value() == '>=10':
            return queryset.filter(inventory__gte=10)

# Model Registering
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders_count']
    list_editable = ['membership']
    list_per_page = 20
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

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


class TagInline(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ['tag']

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_inventory']
    prepopulated_fields = {
        'slug': ['title']
    }
    autocomplete_fields = ['collection']
    search_fields = ['title']
    inlines = [TagInline]
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_name']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', InventoryFilter]
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
    
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} product are successfully updated'
        )

# alternative: admin.StackedInline
class OrderItemInline(admin.TabularInline):  
    model = models.OrderItem
    autocomplete_fields = ['product']
    min_num = 1
    extra = 0

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id', 'placed_at', 'payment_status', 'customer']
    list_per_page = 20
    ordering = ['-placed_at']

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

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

