from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from .views import CustomPasswordResetView, send_test_email, CustomLoginView

urlpatterns = [
    path('', views.home, name='home'),
    path('register_user/', views.RegisterView, name="register_user"),
    path('login_user/', CustomLoginView.as_view(template_name='login.html'), name='login_user'),
    path('logout_user/', views.LogoutView, name='logout_user'),
    path('password_reset/', CustomPasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('send-test-email/', send_test_email, name='send_test_email'),
]


