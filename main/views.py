from django.shortcuts import render


def index(request):
    context = {
        'title': 'Tea shop - Main',
        'content': 'Tea shop',
    }

    return render(request, 'main/index.html', context)


def about(request):
    context = {
        'title': 'Tes shop - About',
        'content': 'About us',
        'text_on_page': "This is a very long text about us",

    }
    return render(request, 'main/about.html', context)
