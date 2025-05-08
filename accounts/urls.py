from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView, register, activate_account, profile

app_name = 'accounts'  # Add namespace for the accounts app

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', register, name='register'),
    path('activate/<str:token>/', activate_account, name='activate'),
    path('profile/', profile, name='profile'),
    path('logout/', LogoutView.as_view(next_page='moviedb:home'), name='logout'),
]