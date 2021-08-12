from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product

def say_hello(request):
    query_set = Product.objects.filter(unit_price__range=(20, 30))

    for product in query_set:
        print(product)
    return render(request, 'hello.html', {'name': 'Pithibi', 'products':list(query_set)})
