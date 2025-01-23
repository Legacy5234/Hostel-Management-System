from django.db import models

#---------------------------------------------------------------------------------------------------------
# HOSTEL MODEL
#---------------------------------------------------------------------------------------------------------
class Hostel(models.Model):
    hostel_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    location = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.hostel_name
    

#---------------------------------------------------------------------------------------------------------
# ROOM MODEL
#---------------------------------------------------------------------------------------------------------
class Room(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=10, null=True)
    capacity = models.IntegerField(default=2)  
    occupants = models.IntegerField(default=0)

    @property
    def occupants_count(self):
        return self.occupants.count 

    def is_available(self):
        return self.occupants < self.capacity

    def __str__(self):
        return f"{self.hostel.hostel_name} - Room {self.room_number}"
    
#---------------------------------------------------------------------------------------------------------
# COMPLAINT MODEL
#---------------------------------------------------------------------------------------------------------
class Complaint(models.Model):
    user = models.ForeignKey('a_userauthapp.User', on_delete=models.CASCADE, related_name='complaints')
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='complaints')
    title = models.CharField(max_length=255)
    description = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ComplaintImage(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='images')
    images = models.ImageField(upload_to='complaint_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.complaint.title}"
