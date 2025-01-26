from django.urls import path
from . import views

app_name = 'a_userauthapp'

urlpatterns = [
    path('login_view/', views.login_view, name='login'),
    path('logout_view/', views.logout_view, name='logout'),

    path('bulk-import-students/', views.bulk_import_students, name='bulk_import_students'),

    path('profile/', views.profile_view, name='student_profile'),  # Current user's profile
    path('profile/<path:matric_number>/', views.profile_view, name='student_profile_detail'),  # View another user's profile
    path('edit_profile/<path:matric_number>/', views.edit_profile, name='edit_profile'),

    path('student_room_complaint/', views.student_room_complaint, name='student_room_complaint'),
]