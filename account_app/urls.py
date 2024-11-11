from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.home, name='home'),
    path('register_user/', views.RegisterView, name="register_user"),
    path('login_user/', LoginView.as_view(template_name='login.html'), name='login_user'),
    path('logout_user/', views.LogoutView, name='logout_user'),
]


