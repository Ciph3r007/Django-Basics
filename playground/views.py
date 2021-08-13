from django.shortcuts import render
from django.db.models import Q
from store.models import Product

def say_hello(request):
    # price between 20 and 30 and inventory > 10
    query_set = Product.objects.filter(unit_price__range=(20, 30), inventory__gt=10)
    # price not between 20 and 30 and inventory > 10
    query_set = Product.objects.filter(~Q(unit_price__range=(20, 30)) | Q(inventory__gt=10))

    for product in query_set:
        print(product)
    return render(request, 'hello.html', {'name': 'Pithibi', 'products':list(query_set)})
