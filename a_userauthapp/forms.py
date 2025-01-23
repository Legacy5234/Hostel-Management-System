from django import forms
from . models import StudentProfile

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        label="Upload CSV File",
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )



class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['image', 'current_level', 'date_of_birth', 'address']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
