from django.urls import path
from .views import admin_dashboard, mark_completed

app_name = 'adminapp'

urlpatterns = [
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('mark_completed/<int:request_id>/', mark_completed, name='mark_completed'),
]
