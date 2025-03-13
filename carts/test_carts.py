import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from carts.models import Cart
from goods.models import Categories, Products


@pytest.fixture
def category_product_user():
    category = Categories.objects.create(name='green_tea', slug='green_tea')
    product = Products.objects.create(name='Product 1', slug='product-1', category=category, quantity=7, price=100)
    user_model = get_user_model()
    user = user_model.objects.create_user(
        first_name='First',
        last_name='Last',
        username='newUser',
        email='newuser@example.com',
        password='testPasswordВ!'
    )
    return category, product, user


@pytest.mark.django_db
def test_cart_add_anonymous(client, category_product_user):
    category, product, _ = category_product_user
    url = reverse('carts:cart_add')
    response = client.post(url, {'product_id': product.id})

    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Product has been added.'


@pytest.mark.django_db
def test_cart_add_authenticated(client, category_product_user):
    _, product, user = category_product_user
    client.login(username="newUser", password="testPasswordВ!")
    url = reverse('carts:cart_add')
    response = client.post(url, {'product_id': product.id})

    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Product has been added.'


@pytest.mark.django_db
def test_cart_add_existing_product(client, category_product_user):
    _, product, user = category_product_user
    client.login(username="newUser", password="testPasswordВ!")
    url = reverse('carts:cart_add')
    response = client.post(url, {'product_id': product.id})
    cart = Cart.objects.get(user=user, product=product)
    cart.refresh_from_db()

    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Product has been added.'
    assert cart.quantity == 1

    response = client.post(url, {'product_id': product.id})

    cart.refresh_from_db()

    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Product quantity has been updated.'
    assert cart.quantity == 2


@pytest.mark.django_db
def test_cart_add_invalid_product(client):
    url = reverse('carts:cart_add')
    response = client.post(url, {'product_id': 99999})

    assert response.status_code == 404
    assert response.json() == {'error': 'Product not found.'}


@pytest.mark.django_db
def test_cart_change_quantity(client, category_product_user):
    _, product, user = category_product_user
    cart = Cart.objects.create(user=user, product=product, quantity=1)
    client.login(username="newUser", password="testPasswordВ!")
    url = reverse('carts:cart_change')

    response = client.post(url, {'cart_id': cart.id, 'quantity': 3})

    cart.refresh_from_db()

    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Amount of product has been changed.'
    assert cart.quantity == 3


@pytest.mark.django_db
def test_cart_remove_product(client, category_product_user):
    _, product, user = category_product_user
    cart = Cart.objects.create(user=user, product=product, quantity=1)
    client.login(username="newUser", password="testPasswordВ!")
    url = reverse('carts:cart_remove')

    response = client.post(url, {'cart_id': cart.id})

    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Product has been removed.'
    assert Cart.objects.count() == 0


@pytest.mark.django_db
def test_cart_remove_invalid_product(client):
    url = reverse('carts:cart_remove')
    response = client.post(url, {'cart_id': 99999})

    assert response.status_code == 404
    assert response.json() == {'error': 'Cart item not found.'}
