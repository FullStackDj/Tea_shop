from django.shortcuts import render

from goods.models import Categories


def index(request):
    categories = Categories.objects.all()

    context = {
        'title': 'Tea shop - Main',
        'content': 'Tea shop',
        'categories': categories,
    }

    return render(request, 'main/index.html', context)


def about(request):
    context = {
        'title': 'Tes shop - About',
        'content': 'About us',
        'text_on_page': "This is a very long text about us",

    }
    return render(request, 'main/about.html', context)
