from django import forms
from .models import WasteRequest

class WasteRequestForm(forms.ModelForm):
    class Meta:
        model = WasteRequest
        fields = ['waste_type', 'quantity', 'collection_time', 'collection_location']
        widgets = {
            'collection_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
