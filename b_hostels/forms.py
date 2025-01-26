from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'block w-full border-gray-300 rounded-md p-2',
                'rows': 4,
                'placeholder': 'Enter complaint title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'block w-full border-gray-300 rounded-md p-2',
                'rows': 8,
                'placeholder': 'Enter detailed description of the issue',
            })
        }


class ComplaintStatusForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select block w-full mt-1',
            }),
        }