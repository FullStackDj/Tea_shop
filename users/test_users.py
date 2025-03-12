import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

from carts.models import Cart
from goods.models import Products, Categories


@pytest.mark.django_db
def test_user_login_view(client):
    user = get_user_model().objects.create_user(username='testUser', password='testPasswordВ!')
    url = reverse('users:login')
    response = client.post(url, {'username': 'testUser', 'password': 'testPasswordВ!'})
    assert response.status_code == 302
    assert response.url == reverse('main:index')
    assert client.session['_auth_user_id'] == str(user.id)


@pytest.mark.django_db
def test_user_registration_view(client):
    url = reverse('users:registration')
    response = client.post(url, {
        'first_name': 'First',
        'last_name': 'Last',
        'username': 'newUser',
        'email': 'newuser@example.com',
        'password1': 'testPasswordВ!',
        'password2': 'testPasswordВ!'

    })
    assert response.status_code == 302
    assert response.url == reverse('users:profile')
    user = get_user_model().objects.get(username='newUser')
    assert user.email == 'newuser@example.com'


@pytest.mark.django_db
def test_user_profile_view(client):
    user = get_user_model().objects.create_user(username='testUser', password='testPasswordВ!')
    client.login(username='testUser', password='testPasswordВ!')
    url = reverse('users:profile')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Profile' in response.context['title']
    assert response.context['user'] == user


@pytest.mark.django_db
def test_user_profile_update(client):
    user = get_user_model().objects.create_user(username='testUser', password='testPasswordВ!')
    client.login(username='testUser', password='testPasswordВ!')
    url = reverse('users:profile')
    response = client.post(url, {
        'first_name': 'UpdatedFirstName',
        'last_name': 'UpdatedLastName',
        'username': 'updateUsername',
        'email': 'updatedemail@example.com'
    })
    user.refresh_from_db()
    assert user.first_name == 'UpdatedFirstName'
    assert user.last_name == 'UpdatedLastName'
    assert user.username == 'updateUsername'
    assert user.email == 'updatedemail@example.com'
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == 'Your profile information has been updated.'


@pytest.mark.django_db
def test_user_cart_view(client):
    category = Categories.objects.create(name='Test Category')
    user = get_user_model().objects.create_user(username='testUser', password='testPasswordВ!')
    client.login(username='testUser', password='testPasswordВ!')
    product = Products.objects.create(name='Test Product', price=10.0, category=category)
    cart = Cart.objects.create(user=user, product=product)
    url = reverse('users:users_cart')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Cart' in response.context['title']
    assert 'user_cart' in response.context
    assert cart in response.context['user_cart']
