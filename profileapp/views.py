from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserProfileForm
# Create your views here.


@login_required
def user_profile(request):
    user = request.user
    return render(request, 'profileapp/profile.html', {"user": user})

# @login_required
# def edit_profile
