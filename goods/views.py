from django.shortcuts import render


def catalog(request):
    context = {
        'title': 'Home - Catalog',
    }
    return render(request, 'goods/catalog.html', context)


def product(request):
    return render(request, 'goods/product.html')
