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
    hostels = Hostel.objects.none()

    if request.user.is_authenticated:
        if not request.user.is_superuser:
            user_gender = request.user.gender
            hostels = Hostel.objects.filter(gender=user_gender).order_by('id')

        elif request.user.is_superuser and request.user.is_male_potter_new_boys:
            hostels = Hostel.objects.filter(hostel_name='New Boys', gender='Male').order_by('id')
        
        elif request.user.is_superuser and request.user.is_male_potter_old_boys:
            hostels = Hostel.objects.filter(hostel_name='Old Boys', gender='Male').order_by('id')

        elif request.user.is_superuser and request.user.is_female_potter_amazon:
            hostels = Hostel.objects.filter(hostel_name='Amazon', gender='Female').order_by('id')

        elif request.user.is_superuser and request.user.is_female_potter_serena:
            hostels = Hostel.objects.filter(hostel_name='Serena', gender='Female').order_by('id')

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

    user_room = request.user.room  

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

    if request.user.room:  
        messages.error(request, f'You have already selected Room {request.user.room.room_number} in {request.user.room.hostel.hostel_name}.')
        return redirect('home')

    if room.occupants < room.capacity:
        request.user.room = room
        request.user.save()
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
    if not request.user.room:  
        messages.error(request, "You are not assigned to any room. Unable to submit a complaint.")
        return redirect('a_userauthapp:student_profile_detail', matric_number=request.user.matric_number)

    room = request.user.room
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.room = room
            complaint.save()

          
            images = request.FILES.getlist('images')  
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


