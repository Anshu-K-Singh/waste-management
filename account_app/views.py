from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.views import PasswordResetView, LoginView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
# Create your views here.

def home(request):
    return render(request, 'index.html')

from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'login.html'  # Specify your custom login template

    def get_success_url(self):
        # If the logged-in user is 'admin', redirect to the dashboard
        if self.request.user.username == 'admin':
            return reverse_lazy('adminapp:dashboard')  # Make sure 'dashboard' is the name of your dashboard view
        # Default redirection (can be home or user-specific landing page)
        return reverse_lazy('home')


def RegisterView(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password != password_confirm:
            messages.error(request, "passwords do not match")
            return redirect('register_user')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "username already exists")
            return redirect('register_user')
         
        if User.objects.filter(email=email).exists():
            messages.error(request, "email already exists")
            return redirect('register_user')
        
        
        user = User.objects.create_user(
            username = username,
            email = email,
            first_name = first_name,
            last_name = last_name,
            password = password
        )
        messages.success(request, "Regsitration succesful please login ")
        return redirect('login_user')

    return render(request, 'register.html')


def LogoutView(request):
    logout(request)
    return redirect("/login_user")


class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        print("Sending email...")
        response = super().form_valid(form)
        print("Email sent successfully!")
        return response
       
def send_test_email(request):
    subject = 'Test Email'
    message = "message"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ["anshu@gmail.com"]
    
    send_mail = (subject, message, from_email, recipient_list)
    return HttpResponse("test emailsend check your console")