from django.shortcuts import render
from django.db.models import Q, F
from store.models import Product, OrderItem, Order

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

    # Inner Join
    # [for many to 1]
    query_set = Product.objects.select_related('collection')
    # [for many to many]
    query_set = Product.objects.prefetch_related('promotions')

    # last 5 orders with customer and items
    query_set = Order.objects.select_related('customer').order_by('-placed_at')[:5]\
                             .prefetch_related('orderitem_set__product')


    for product in query_set:
        print(product)
    return render(request, 'hello.html', {'name': 'Pithibi', 'orders':list(query_set)})
