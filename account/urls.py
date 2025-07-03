from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import UserLoginView, UserRegistrationView, DashboardView, ProfileEditView

app_name = 'account'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='account:login'), name='logout'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/', ProfileEditView.as_view(), name='profile'),

    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
