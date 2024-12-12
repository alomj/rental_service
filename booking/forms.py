from django import forms
from .models import Ticket

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class BuyTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['passenger_name', 'email']
        widgets = {
            'passenger_name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'email': forms.EmailInput(attrs={
                'class': INPUT_CLASSES
            })
        }
