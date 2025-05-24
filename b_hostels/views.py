from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from a_userauthapp.models import User
from .models import Room,Complaint
from .forms import ComplaintStatusForm
from django.core.paginator import Paginator

#---------------------------------------------------------------------------------------------------------
# ADMIN STUDENT ROOM MANAGEMENT VIEW
#---------------------------------------------------------------------------------------------------------
@login_required(login_url='a_userauthapp:login')
def admin_manage_users_in_room(request):
    # Get all rooms
    rooms = Room.objects.all()
    complaint_count = Complaint.objects.count()

    # Filter users based on admin's role
    if request.user.is_male_potter_new_boys:
        users = User.objects.filter(is_superuser=False, gender='Male') 
    elif request.user.is_male_potter_old_boys:
        users = User.objects.filter(is_superuser=False, gender='Male')
    elif request.user.is_female_potter_amazon:
        users = User.objects.filter(is_superuser=False, gender='Female')
    elif request.user.is_female_potter_serena:
        users = User.objects.filter(is_superuser=False, gender='Female')  
    else:
        users = User.objects.all()

    context = {
        'rooms': rooms,
        'users': users,
        'complaint_count':complaint_count
    }
    return render(request, 'b_hostel/admin_room_management.html', context)


#---------------------------------------------------------------------------------------------------------
# ADMIN STUDENT ROOM COMPLAINT MANAGEMENT VIEW
#---------------------------------------------------------------------------------------------------------
def all_complaints(request):
    complaints = Complaint.objects.prefetch_related('images').select_related('user', 'room')
    paginator = Paginator(complaints, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        complaint_id = request.POST.get('complaint_id')
        complaint = get_object_or_404(Complaint, id=complaint_id)
        form = ComplaintStatusForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            messages.success(request, f"The status for '{complaint.title}' has been updated.")
            return redirect('b_hostels:all_complaints')
        else:
            messages.error(request, "Failed to update the complaint status. Please try again.")

    context = {'page_obj': page_obj, 'form': ComplaintStatusForm()} 
    return render(request, 'b_hostel/complaints.html', context)

