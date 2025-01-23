from django.urls import path
from . import views

app_name = 'b_hostels'

urlpatterns = [
    path('manage_users_in_room/', views.admin_manage_users_in_room, name='admin_manage_users_in_room'),
    path('all-complaints/', views.all_complaints, name='all_complaints'),
]
