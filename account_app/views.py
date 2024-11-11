from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'index.html')


def RegisterView(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']

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