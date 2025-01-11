from django import forms
from .models import Ticket, Rental, Car

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


class CarRentalForm(forms.ModelForm):
    rental_start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': INPUT_CLASSES
        }),
        label="Date of beginning rent"
    )
    rental_end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': INPUT_CLASSES
        }),
        label="Date of end renting"
    )

    def __init__(self, *args, **kwargs):
        self.car = kwargs.pop('car', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        rental_start_date = cleaned_data.get('rental_start_date')
        rental_end_date = cleaned_data.get('rental_end_date')

        if rental_start_date and rental_end_date:
            if rental_start_date > rental_end_date:
                raise forms.ValidationError("The start date of the car rental cannot be later than the end date.")
            rental_days = (rental_end_date - rental_start_date).days
            if self.car:
                cleaned_data['total_price'] = rental_days * self.car.price_per_day
            else:
                raise forms.ValidationError("Car information is missing.")

        return cleaned_data

    class Meta:
        model = Rental
        fields = ['rental_start_date', 'rental_end_date']





