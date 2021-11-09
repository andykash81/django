from django.shortcuts import render, redirect
from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    phones = Phone.objects.all()
    request_sort = request.GET.get('sort')
    if request_sort == 'name':
        sort = phones.order_by('name')
    elif request_sort == 'min_price':
        sort = phones.order_by('price')
    elif request_sort == 'max_price':
        sort = phones.order_by('-price')
    else:
        sort = phones
    context = {
        'phones': sort
    }
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.filter(slug=slug).values()
    context = {
        'phone': phone[0]
    }
    return render(request, template, context)
