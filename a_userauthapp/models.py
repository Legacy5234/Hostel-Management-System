from django.db import models
from b_hostels.models import Room

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

#---------------------------------------------------------------------------------------------------------
# ACCOUNT MANAGER MODEL
#---------------------------------------------------------------------------------------------------------
class StaffAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, matric_number, dept, gender, password):
        if not first_name:
            raise ValueError('First name is missing')
        if not last_name:
            raise ValueError('Last name is missing')
        if not matric_number:
            raise ValueError('Matric number is missing')
        if not dept:
            raise ValueError('Department number is missing')
        if not gender:
            raise ValueError('Gender is missing')
        if not password:
            raise ValueError('Password is missing')

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            matric_number=matric_number,
            dept=dept
        )
        user.set_password(password)  # Use the provided password
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, matric_number, dept, gender, password):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            matric_number=matric_number,
            dept=dept,
            password=password
        )
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user


#---------------------------------------------------------------------------------------------------------
# CUSTOM USER MODEL
#---------------------------------------------------------------------------------------------------------
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    matric_number = models.CharField(max_length=9, unique=True, blank=False)
    gender = models.CharField(max_length=25, choices=[('Male', 'Male'), ('Female', 'Female')], null=True)
    dept = models.CharField(max_length=100, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    is_male_potter_new_boys = models.BooleanField(default=False)
    is_male_potter_old_boys = models.BooleanField(default=False)

    is_female_potter_amazon = models.BooleanField(default=False)
    is_female_potter_serena = models.BooleanField(default=False)

    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')

    USERNAME_FIELD = 'matric_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender', 'dept']

    objects = StaffAccountManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
#---------------------------------------------------------------------------------------------------------
# STUDENT PROFILE MODEL
#---------------------------------------------------------------------------------------------------------
# Images Directory For Users
def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/{filename}'

from django.templatetags.static import static

CURRENT_LEVEL = (
    ('100','100'),
    ('200','200'),
    ('300','300'),
    ('400','400'),
    ('500','500'),
    ('600','600'),
)
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    current_level = models.CharField(max_length=3, choices=CURRENT_LEVEL, null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name}'s Profile"
    
    @property
    def image_url(self):
        return self.image.url if self.image else static('images/default-profilepic.png')

   
