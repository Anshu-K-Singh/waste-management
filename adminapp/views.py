from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from wasteapp.models import WasteRequest
from django.utils import timezone


def admin_dashboard(request):
    # Fetch all waste collection requests
    all_requests = WasteRequest.objects.all().order_by('-created_at')
    context = {'all_requests': all_requests}
    return render(request, 'adminapp/admin_dashboard.html', context)


def mark_completed(request, request_id):
    waste_request = WasteRequest.objects.get(id=request_id)
    waste_request.status = 'Completed'
    waste_request.completed_at = timezone.now()
    waste_request.save()
    return redirect('adminapp:admin_dashboard')