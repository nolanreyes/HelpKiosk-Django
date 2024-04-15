from django import forms
from .models import Bed


class BedForm(forms.ModelForm):
    class Meta:
        model = Bed
        fields = ['bed_number', 'is_occupied']
        labels = {
            'bed_number': 'Bed Number',
            'is_occupied': 'Is Occupied',
        }
        help_texts = {
            'bed_number': 'Enter the bed number within the room.',
            'is_occupied': 'Mark this if the bed is currently occupied.',
        }
