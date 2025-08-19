from django.contrib.auth.views import LoginView
from django.urls import path, include
from .forms import UserLoginForm
from .views import RegisterView, ProfileView, StudentUpdateView


urlpatterns = [
    path('profile/<int:user_id>/', ProfileView.as_view(), name='Profile'),
    path('profile/<int:user_id>/edit/', StudentUpdateView.as_view(), name='EditProfile'),
    path('login/', LoginView.as_view(authentication_form=UserLoginForm), name='Login'),
    path('register/', RegisterView.as_view(), name='Register'),
    path('', include('django.contrib.auth.urls')),
]
