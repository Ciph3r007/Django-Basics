from django.db.models.fields import DecimalField
from django.shortcuts import render
from django.db.models import Q, F, Value, Func, Count, Avg, ExpressionWrapper
from django.db.models.functions import Concat
from store.models import Customer, Product, OrderItem, Order

def say_hello(request):
    # price between 20 and 30 and inventory > 10
    query_set = Product.objects.filter(unit_price__range=(20, 30), inventory__gt=10)
    # price not between 20 and 30 and inventory > 10
    query_set = Product.objects.filter(~Q(unit_price__range=(20, 30)) | Q(inventory__gt=10))
    # inventory = collection_id
    query_set = Product.objects.filter(inventory=F('collection__id'))
    # sorting
    query_set = Product.objects\
                       .filter(unit_price__range=(20, 30), inventory__gt=10)\
                       .order_by('-unit_price', 'title')
    # sem shite
    query_set = Product.objects\
                       .filter(unit_price__range=(20, 30), inventory__gt=10)\
                       .order_by('unit_price', '-title').reverse()

    # select and limit
    query_set = Product.objects.all() # returns objects
    query_set = Product.objects.only('title')[5:10]  # returns objects (out of column access will result in multiple queries)
    query_set = Product.objects.values('title')[5:10] # returns dictionary ((out of column access will return null))
    query_set = Product.objects.values_list('title', 'unit_price')[5:10] # returns tuples (no column access, only values)
    query_set = Product.objects.defer('title')[5:10] # returns objects [inverse selection]

    # products that have been ordered
    query_set = Product.objects.filter(
        id__in=OrderItem.objects.values('product_id').distinct())\
            .order_by('title') # values_list is usable too

    # Joins
    # [for many to 1]
    query_set = Product.objects.select_related('collection')
    # [for many to many]
    query_set = Product.objects.prefetch_related('promotions')

    # last 5 orders with customer and items
    query_set = Order.objects.select_related('customer').order_by('-placed_at')[:5]\
                             .prefetch_related('orderitem_set__product')
    
    # annotated column
    query_set = Customer.objects.annotate(
        full_name=Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT')
    )
    # SEM SHITE
    query_set = Customer.objects.annotate(
        full_name=Concat('first_name', Value(' '), 'last_name')
    )

    # aggregate functions
    query_set = Product.objects.aggregate(Avg('unit_price'))

    # orders of customers using group by
    # 1 to many relationship, but should use 'order' instead of 'order_set'
    # weird flex but ok!
    query_set = Customer.objects.annotate(
        order_count = Count('order')
    )

    # Expression Wrapper
    discounted_price = ExpressionWrapper(
        F('unit_price') * 0.8, output_field=DecimalField()
    )
    query_set = Product.objects.annotate(
        discounted_price=discounted_price
    )
    
    return render(request, 'hello.html', {'name': 'Pithibi', 'orders':list(query_set)})
