from django.shortcuts import render
from django.db.models import Q, F
from store.models import Product

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
    

    for product in query_set:
        print(product)
    return render(request, 'hello.html', {'name': 'Pithibi', 'products':list(query_set)})
