import pytest
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.urls import reverse

from carts.models import Cart
from goods.models import Products, Categories
from orders.models import Order


@pytest.mark.django_db
def test_create_order_multiple_items(client):
    user = get_user_model().objects.create_user(username='testUser', password='testPasswordВ!')
    client.login(username='testUser', password='testPasswordВ!')

    category = Categories.objects.create(name='Test Category', slug='test-category')
    product1 = Products.objects.create(name='Test Product 1', price=100.0, quantity=5, category=category)
    product2 = Products.objects.create(name='Test Product 2', price=200.0, quantity=10, category=category)

    Cart.objects.create(user=user, product=product1, quantity=2)
    Cart.objects.create(user=user, product=product2, quantity=1)

    order_data = {
        'first_name': 'FirstName',
        'last_name': 'LastName',
        'phone_number': '123456789012',
        'requires_delivery': 1,
        'delivery_address': 'Test Address',
        'payment_on_get': 1,
    }

    url = reverse('orders:create_order')
    response = client.post(url, order_data)

    assert response.status_code == 302
    assert response.url == reverse('users:profile')

    order = Order.objects.get(user=user)
    assert order.user == user
    assert order.orderitem_set.count() == 2

    product1.refresh_from_db()
    product2.refresh_from_db()

    assert product1.quantity == 3
    assert product2.quantity == 9


@pytest.mark.django_db
def test_create_order_no_delivery_address(client):
    user = get_user_model().objects.create_user(username='testUser', password='testPasswordВ!')
    client.login(username='testUser', password='testPasswordВ!')

    category = Categories.objects.create(name='Test Category', slug='test-category')
    product = Products.objects.create(name='Test Product', price=100.0, quantity=10, category=category)

    Cart.objects.create(user=user, product=product, quantity=2)

    order_data = {
        'first_name': 'FirstName',
        'last_name': 'LastName',
        'phone_number': '123456789012',
        'requires_delivery': 0,
        'delivery_address': '',
        'payment_on_get': 1,
    }

    url = reverse('orders:create_order')
    response = client.post(url, order_data)

    assert response.status_code == 302
    assert response.url == reverse('users:profile')

    order = Order.objects.get(user=user)
    assert order.requires_delivery == 0
    assert order.delivery_address == ''


@pytest.mark.django_db
def test_create_order_insufficient_stock_with_multiple_items(client):
    user = get_user_model().objects.create_user(username='testUser', password='testPasswordВ!')
    client.login(username='testUser', password='testPasswordВ!')

    category = Categories.objects.create(name='Test Category', slug='test-category')
    product1 = Products.objects.create(name='Test Product 1', price=100.0, quantity=1, category=category)
    product2 = Products.objects.create(name='Test Product 2', price=200.0, quantity=2, category=category)

    Cart.objects.create(user=user, product=product1, quantity=2)
    Cart.objects.create(user=user, product=product2, quantity=2)

    order_data = {
        'first_name': 'FirstName',
        'last_name': 'LastName',
        'phone_number': '123456789012',
        'requires_delivery': 1,
        'delivery_address': 'Test Address',
        'payment_on_get': 1,
    }

    url = reverse('orders:create_order')
    response = client.post(url, order_data)

    assert response.status_code == 302
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert 'Not enough quantity product' in str(messages[0])


@pytest.mark.django_db
def test_cart_is_emptied_after_order_creation(client):
    user = get_user_model().objects.create_user(username='testUser', password='testPasswordВ!')
    client.login(username='testUser', password='testPasswordВ!')

    category = Categories.objects.create(name='Test Category', slug='test-category')
    product = Products.objects.create(name='Test Product', price=100.0, quantity=10, category=category)

    Cart.objects.create(user=user, product=product, quantity=2)

    order_data = {
        'first_name': 'FirstName',
        'last_name': 'LastName',
        'phone_number': '123456789012',
        'requires_delivery': 1,
        'delivery_address': 'Test Address',
        'payment_on_get': 1,
    }

    url = reverse('orders:create_order')
    client.post(url, order_data)

    assert Cart.objects.filter(user=user).count() == 0
