from django.urls import path
from django.contrib.auth.views import LogoutView

from . views import RegistrationView, LoginView, AccountView


app_name = 'account'


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('accounts/', AccountView.as_view(), name='accounts'),
]