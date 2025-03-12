import pytest
from django.core.cache import cache
from django.urls import reverse
from .models import Page


@pytest.mark.django_db
def test_index_view(client):
    Page.objects.create(title='Home', content='Welcome to the home page!')
    response = client.get(reverse('main:index'))
    assert response.status_code == 200
    assert response.context['title'] == 'Home'
    assert response.context['content'] == 'Welcome to the home page!'
    assert 'main/index.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_about_view(client):
    cache.clear()
    Page.objects.create(title='About', content='This is the about page.', text_on_page='Some additional text.')
    response = client.get(reverse('main:about'))
    assert response.status_code == 200
    assert response.context['title'] == 'About'
    assert response.context['content'] == 'This is the about page.'
    assert response.context['text_on_page'] == 'Some additional text.'
    assert 'main/about.html' in [t.name for t in response.templates]
