from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import csv
from .forms import StudentProfileForm,CSVUploadForm
from .models import User,StudentProfile

from b_hostels.models import Room,Complaint

# Create your views here.
#---------------------------------------------------------------------------------------------------------
# LOGIN VIEW
#---------------------------------------------------------------------------------------------------------
def login_view(request):
    if request.method == 'POST':
        matric_number = request.POST.get('matric_number')
        password = request.POST.get('password')

        user = authenticate(request, matric_number=matric_number, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f'Welcome {user.first_name} {user.last_name}')
                return redirect('home')
            else:
                messages.error(request, 'This account has been suspended..')
        else:
            messages.error(request, 'Invalid credentials,Please try again with valid credentials..')
    return render(request, 'a_userauthapp/login.html')


#---------------------------------------------------------------------------------------------------------
# LOGOUT VIEW
#---------------------------------------------------------------------------------------------------------
def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out..')
    return redirect('a_userauthapp:login')



#---------------------------------------------------------------------------------------------------------
# STUDENT DATA BULK IMPORT VIEW
#---------------------------------------------------------------------------------------------------------
@login_required(login_url='a_userauthapp:login')
def bulk_import_students(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']

            try:
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)

                success_count = 0
                error_count = 0
                errors = []

                for row in reader:
                    matric_number = row.get('matric_number')
                    first_name = row.get('first_name')
                    last_name = row.get('last_name')
                    gender = row.get('gender', '').capitalize() 
                    dept = row.get('dept', '').strip() 
                    password = row.get('password', matric_number)  

            
                    if not matric_number or not first_name or not last_name or not gender or not dept:
                        errors.append(f"Missing data in row: {row}")
                        error_count += 1
                        continue

                    if gender not in ['Male', 'Female']:
                        errors.append(f"Invalid gender '{gender}' for matric number {matric_number}.")
                        error_count += 1
                        continue

                    if len(dept) == 0:
                        errors.append(f"Invalid or missing department for matric number {matric_number}.")
                        error_count += 1
                        continue

                    if User.objects.filter(matric_number=matric_number).exists():
                        errors.append(f"Matric number {matric_number} already exists.")
                        error_count += 1
                        continue

                    try:
                        User.objects.create_user(
                            matric_number=matric_number,
                            first_name=first_name,
                            last_name=last_name,
                            gender=gender,
                            dept=dept, 
                            password=password,
                        )
                        success_count += 1
                    except Exception as e:
                        errors.append(f"Error creating student for matric number {matric_number}: {str(e)}")
                        error_count += 1

                if success_count > 0:
                    messages.success(request, f"{success_count} students imported successfully.")
                if error_count > 0:
                    messages.error(request, f"{error_count} errors occurred during import.")
                    for error in errors:
                        messages.error(request, error)

                return redirect('a_userauthapp:bulk_import_students')
            except Exception as e:
                messages.error(request, f"Error reading the file: {str(e)}")
    else:
        form = CSVUploadForm()

    return render(request, 'a_userauthapp/bulk_import_students.html', {'form': form})


#---------------------------------------------------------------------------------------------------------
# STUDENT PROFILE VIEW
#---------------------------------------------------------------------------------------------------------
@login_required(login_url='a_userauthapp:login')
def profile_view(request, matric_number=None):
    if matric_number:
        user = get_object_or_404(User, matric_number=matric_number)
        profile = user.profile
    else:
        profile = request.user.profile

    if request.user.is_superuser and request.user.is_male_potter_new_boys:
        rooms = Room.objects.filter(hostel__hostel_name='New Boys', hostel__gender='Male')
    elif request.user.is_superuser and request.user.is_male_potter_old_boys:
        rooms = Room.objects.filter(hostel__hostel_name='Old Boys', hostel__gender='Male')
    elif request.user.is_superuser and request.user.is_female_potter_amazon:
        rooms = Room.objects.filter(hostel__hostel_name='Amazon', hostel__gender='Female')
    elif request.user.is_superuser and request.user.is_female_potter_serena:
        rooms = Room.objects.filter(hostel__hostel_name='Serena', hostel__gender='Female')
    else:
        rooms = Room.objects.none()
        
    if request.method == 'POST':
        action = request.POST.get('action')
        room_id = request.POST.get('room')

        if not room_id:
            messages.error(request, "Please select a valid room.")
        else:
            room = get_object_or_404(Room, id=room_id)

            if action == 'add':
                if user.room:  
                    messages.error(request, f'{user.first_name} {user.last_name} is already assigned to Room {user.room.room_number}.')
                elif room.occupants >= room.capacity:
                    messages.error(request, f'Room {room.room_number} is full.')
                else:
                    # Assign user to the room
                    user.room = room
                    user.save()
                    room.occupants += 1
                    room.save()
                    messages.success(request, f'{user.first_name} {user.last_name} has been added to Room {room.room_number}.')
            elif action == 'remove':
                if user.room == room:  # User is in the selected room
                    # Remove user from the room
                    user.room = None
                    user.save()
                    room.occupants -= 1
                    room.save()
                    messages.success(request, f'{user.first_name} {user.last_name} has been removed from Room {room.room_number}.')
                else:
                    messages.error(request, f'{user.first_name} {user.last_name} is not assigned to Room {room.room_number}.')
        return redirect('a_userauthapp:student_profile_detail', matric_number=user.matric_number)

    context = {
        'profile': profile,
        'rooms': rooms,
    }
    return render(request, 'a_userauthapp/student_profile.html', context)


#---------------------------------------------------------------------------------------------------------
# STUDENT PROFILE EDIT VIEW
#---------------------------------------------------------------------------------------------------------
def edit_profile(request, matric_number):
    try:
        user = User.objects.get(matric_number=matric_number)  # Get the user by matric_number
        profile = user.profile  # Access the profile for this user
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('home')  # Redirect if the user does not exist
    except StudentProfile.DoesNotExist:
        messages.error(request, "Profile not found. Please create your profile.")
        return redirect('home')  # Redirect to profile creation page if no profile

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('a_userauthapp:student_profile_detail', matric_number=matric_number)
        else:
            messages.error(request, "There was an error updating your profile. Please correct the errors below.")
    else:
        form = StudentProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
        'user': user,
    }

    return render(request, 'a_userauthapp/edit_profile.html', context)


#---------------------------------------------------------------------------------------------------------
# STUDENT ROOM COMPLAIN VIEW
#---------------------------------------------------------------------------------------------------------
def student_room_complaint(request):
    complaints = Complaint.objects.filter(user=request.user)
    return render(request, 'b_hostel/student_complain.html', {'complaints':complaints})

