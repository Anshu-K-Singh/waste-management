from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile, Address
from .forms import UserProfileForm, AddressForm
from django.shortcuts import get_object_or_404
# Create your views here.


@login_required
def user_profile(request):
    """
    View to display the user's profile.
    """
    user = request.user
    addresses = Address.objects.filter(user=user)
    try:
        user_profile = user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = None  # In case the user doesn't have a profile

    return render(request, 'profileapp/profile.html', {
        'user_profile': user_profile,
        'addresses': addresses
    })

@login_required
def edit_profile(request):
    """
    View to edit the user's profile.
    """
    user = request.user
    try:
        user_profile = user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=user)

    if request.method == "POST":
        user_form = UserProfileForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profileapp:user_profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserProfileForm(instance=user)

    return render(request, 'profileapp/edit_profile.html', {
        'form': user_form,
    })


@login_required
def add_address(request):
    """
    View to allow the user to add a new address.
    """
    if request.method == "POST":
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            # Save the address, associating it with the logged-in user
            new_address = address_form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            messages.success(request, "Address added successfully!")
            return redirect('profileapp:user_profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        address_form = AddressForm()

    return render(request, 'profileapp/add_address.html', {
        'form': address_form,
    })
    


@login_required
def delete_address(request, address_id):
    """
    View to allow the user to delete an address.
    """
    address = get_object_or_404(Address, id=address_id, user=request.user)
    
    if request.method == "POST":
        address.delete()
        messages.success(request, "Address deleted successfully!")
        return redirect('profileapp:user_profile')

    return render(request, 'profileapp/delete_address.html', {
        'address': address,
    })


@login_required
def set_default_address(request, address_id):
    """
    View to set a default address for the logged-in user.
    """
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.default = True
    address.save()
    messages.success(request, "Default address updated successfully!")
    return redirect('profileapp:user_profile')