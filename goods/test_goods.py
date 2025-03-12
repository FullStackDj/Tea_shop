import pytest
from django.urls import reverse
from goods.models import Products, Categories
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
def test_catalog_view_with_category(client):
    category = Categories.objects.create(name='green_tea', slug='green_tea')
    Products.objects.create(name='Product 1', slug='product-1', category=category, price=100)
    Products.objects.create(name='Product 2', slug='product-2', category=category, price=200)

    url = reverse('goods:index', kwargs={'category_slug': category.slug})
    response = client.get(url)

    assert response.status_code == 200
    assert 'goods' in response.context
    assert len(response.context['goods']) == 2
    assert response.context['title'] == 'Catalog'


@pytest.mark.django_db
def test_catalog_view_with_search(client):
    category = Categories.objects.create(name='green_tea', slug='green_tea')
    Products.objects.create(name='Searchable Product', slug='searchable-product', category=category, price=100)

    url = reverse('goods:search') + '?q=Searchable'
    response = client.get(url)

    assert response.status_code == 200
    assert 'goods' in response.context
    assert len(response.context['goods']) == 1


@pytest.mark.django_db
def test_catalog_view_no_goods_found(client):
    url = reverse('goods:index', kwargs={'category_slug': 'nonexistent-category'})
    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_product_view(client):
    category = Categories.objects.create(name='green_tea', slug='green_tea')
    product = Products.objects.create(name='Test Product', slug='test-product', category=category, price=100)

    image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
    product.image = image
    product.save()

    url = reverse('goods:product', kwargs={'product_slug': product.slug})
    response = client.get(url)

    assert response.status_code == 200
    assert 'product' in response.context
    assert response.context['product'] == product
    assert response.context['title'] == product.name


@pytest.mark.django_db
def test_product_view_404(client):
    url = reverse('goods:product', kwargs={'product_slug': 'nonexistent-product'})
    response = client.get(url)

    assert response.status_code == 404
