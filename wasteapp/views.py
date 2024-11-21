from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import WasteRequestForm
from .models import WasteRequest
from profileapp.models import Address


@login_required
def submit_waste_request(request):
    if request.method == 'POST':
        form = WasteRequestForm(request.POST, user=request.user)  # Pass user context to the form
        if form.is_valid():
            waste_request = form.save(commit=False)
            waste_request.user = request.user  # Associate the request with the logged-in user

            # Check if an address was selected
            if not form.cleaned_data.get('collection_location'):
                # Use default address if no address is selected
                default_address = Address.objects.filter(user=request.user, is_default=True).first()
                if default_address:
                    waste_request.collection_location = default_address
                else:
                    messages.error(request, "No default address found. Please select an address.")
                    return redirect('wasteapp:submit_request')
            else:
                # Save the selected address
                waste_request.collection_location = form.cleaned_data.get('collection_location')

            # Save the waste request
            waste_request.save()
            messages.success(request, 'Waste collection request submitted successfully!')
            return redirect('wasteapp:my_requests')
    else:
        # Pass user context to the form to filter addresses
        form = WasteRequestForm(user=request.user)

    # Add the form to the context
    context = {'form': form}
    return render(request, 'wasteapp/submit_request.html', context)


@login_required
def my_requests(request):
    # Fetch only the pending requests of the logged-in user
    pending_requests = WasteRequest.objects.filter(user=request.user, status='Pending').order_by('-created_at')
    
    context = {'pending_requests': pending_requests}
    return render(request, 'wasteapp/my_requests.html', context)

@login_required
def mark_as_completed(request, request_id):
    try:
        # Fetch the specific request by ID and verify it belongs to the logged-in user
        waste_request = WasteRequest.objects.get(id=request_id, user=request.user, status='Pending')
        waste_request.status = 'Completed'
        waste_request.save()
        messages.success(request, 'Request marked as completed.')
    except WasteRequest.DoesNotExist:
        messages.error(request, 'Request not found or already completed.')

    return redirect('wasteapp:my_requests')


@login_required
def my_history(request):
    # Fetch only the completed requests of the logged-in user
    completed_requests = WasteRequest.objects.filter(user=request.user, status='Completed').order_by('-created_at')
    
    context = {'completed_requests': completed_requests}
    return render(request, 'wasteapp/my_history.html', context)