from django.contrib import admin
from . models import Hostel,Room,Complaint,ComplaintImage

# Register your models here.
admin.site.register(Hostel)
admin.site.register(Room)
admin.site.register(Complaint)
admin.site.register(ComplaintImage)