from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from wasteapp.models import WasteRequest
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User


# def admin_dashboard(request):
#     # Fetch all waste collection requests
#     all_requests = WasteRequest.objects.all().order_by('-created_at')
#     context = {'all_requests': all_requests}
#     return render(request, 'adminapp/admin_dashboard.html', context)


# def mark_completed(request, request_id):
#     waste_request = WasteRequest.objects.get(id=request_id)
#     waste_request.status = 'Completed'
#     waste_request.completed_at = timezone.now()
#     waste_request.save()
#     return redirect('adminapp:admin_dashboard')

from django.contrib.auth.models import User

def admin_dashboard(request):
    total_requests = WasteRequest.objects.count()
    pending_requests = WasteRequest.objects.filter(status="Pending").count()
    rejected_requests = WasteRequest.objects.filter(status="Rejected").count()
    completed_requests = WasteRequest.objects.filter(status="Completed").count()
    total_users = User.objects.count()

    context = {
        "total_requests": total_requests,
        "pending_requests": pending_requests,
        "rejected_requests": rejected_requests,
        "completed_requests": completed_requests,
        "total_users": total_users,
    }
    return render(request, "adminapp/dashboard.html", context)


def manage_pending_requests(request):
    pending_requests = WasteRequest.objects.filter(status="Pending").order_by("-created_at")
    context = {"pending_requests": pending_requests}
    return render(request, "adminapp/pending_requests.html", context)

def approve_request(request, request_id):
    waste_request = get_object_or_404(WasteRequest, id=request_id)
    waste_request.status = "Completed"
    waste_request.save()
    return redirect("adminapp:manage_pending_requests")

def reject_request(request, request_id):
    waste_request = get_object_or_404(WasteRequest, id=request_id)
    waste_request.status = "Rejected"
    waste_request.save()
    return redirect("adminapp:manage_pending_requests")


def view_completed_requests(request):
    completed_requests = WasteRequest.objects.filter(status="Completed").order_by("-created_at")
    context = {"completed_requests": completed_requests}
    return render(request, "adminapp/completed_requests.html", context)



def manage_users(request):
    users = User.objects.all()  # Fetch all users
    context = {"users": users}
    return render(request, "adminapp/manage_users.html", context)

def toggle_user_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_active:
        user.is_active = False
        messages.success(request, f"User {user.username} has been deactivated.")
    else:
        user.is_active = True
        messages.success(request, f"User {user.username} has been reactivated.")
    user.save()
    return redirect("adminapp:manage_users")

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    messages.success(request, f"User {user.username} has been deleted.")
    user.delete()
    return redirect("adminapp:manage_users")
