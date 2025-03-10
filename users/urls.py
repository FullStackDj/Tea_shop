from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import UserLoginView, UserRegistrationView, UserProfileView, UserCartView

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('users-cart/', UserCartView.as_view(), name='users_cart'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
