from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from b_hostels.models import Hostel,Room,ComplaintImage
from b_hostels.forms import ComplaintForm

#---------------------------------------------------------------------------------------------------------
# HOMEPAGE VIEW
#---------------------------------------------------------------------------------------------------------
@login_required(login_url='a_userauthapp:login')
def homepage(request):
    # Initialize hostels as an empty queryset to avoid errors
    hostels = Hostel.objects.none()

    if request.user.is_authenticated:
        # For regular authenticated users
        if not request.user.is_superuser:
            user_gender = request.user.gender
            hostels = Hostel.objects.filter(gender=user_gender)

        # For male potters (admins managing male hostels)
        elif request.user.is_superuser and request.user.is_male_potter:
            hostels = Hostel.objects.filter(gender='Male')

        # For female potters (admins managing female hostels)
        elif request.user.is_superuser and request.user.is_female_potter:
            hostels = Hostel.objects.filter(gender='Female')

    context = {
        'hostels': hostels
    }
    return render(request, 'HMS/home.html', context)


#---------------------------------------------------------------------------------------------------------
# HOSTEL DETAIL VIEW
#---------------------------------------------------------------------------------------------------------
@login_required(login_url='a_userauthapp:login')
def hostel_detail(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    rooms = Room.objects.filter(hostel=hostel)

    # Check if the user already occupies a room
    user_room = request.user.room  # Access user's room directly via the ForeignKey

    context = {
        'hostel': hostel,
        'rooms': rooms,
        'user_room': user_room,
    }
    return render(request, 'b_hostel/hostel_detail.html', context)


#---------------------------------------------------------------------------------------------------------
# ROOM SELECTION VIEW
#---------------------------------------------------------------------------------------------------------
@login_required(login_url='a_userauthapp:login')
def select_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    # Check if the user already occupies a room
    if request.user.room:  # Access user's room directly
        messages.error(request, f'You have already selected Room {request.user.room.room_number} in {request.user.room.hostel.hostel_name}.')
        return redirect('home')

    # Check room availability based on capacity
    if room.occupants < room.capacity:
        # Assign the user to the room
        request.user.room = room
        request.user.save()

        # Increment the room's occupant count
        room.occupants += 1
        room.save()

        messages.success(request, f'You have successfully selected Room {room.room_number}.')
    else:
        messages.error(request, 'Room is no longer available.')

    return redirect('home')


#---------------------------------------------------------------------------------------------------------
# ROOM COMPLAINT VIEW
#---------------------------------------------------------------------------------------------------------
@login_required(login_url='a_userauthapp:login')
def submit_complaint(request):
    if not request.user.room:  # Ensure the user has a room assigned
        messages.error(request, "You are not assigned to any room. Unable to submit a complaint.")
        return redirect('a_userauthapp:student_profile_detail', matric_number=request.user.matric_number)

    room = request.user.room  # Get the user's current room
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the complaint first
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.room = room
            complaint.save()

            # Handle multiple file uploads for complaint images
            images = request.FILES.getlist('images')  # Get all uploaded files with the name 'images'
            for image in images:
                ComplaintImage.objects.create(complaint=complaint, images=image)

            messages.success(request, "Your complaint has been successfully submitted.")
            return redirect('a_userauthapp:student_profile_detail', matric_number=request.user.matric_number)
        else:
            messages.error(request, "There was an error submitting your complaint. Please try again.")
    else:
        form = ComplaintForm()

    context = {
        'form': form,
        'room': room,
    }
    return render(request, 'b_hostel/submit_complaint.html', context)


