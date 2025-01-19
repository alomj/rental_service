from django import forms

from .models import Ticket, Rental, Hotel

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


class HotelRentalForm(forms.ModelForm):
    arrival_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': INPUT_CLASSES
        }),
        label="Date of Arrival"
    )
    departure_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': INPUT_CLASSES
        }),
        label="Date of Departure"
    )

    def __init__(self, *args, **kwargs):
        self.hotel = kwargs.pop('hotel', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        arrival_date = cleaned_data.get('arrival_date')
        departure_date = cleaned_data.get('departure_date')

        if arrival_date and departure_date:
            if arrival_date > departure_date:
                raise forms.ValidationError("The arrival date cannot be later than the departure date.")

            rental_days = (departure_date - arrival_date).days


            cleaned_data['total_price'] = rental_days * self.hotel.price_per_night
        else:
            raise forms.ValidationError("Both arrival and departure dates are required.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.hotel = self.hotel
        instance.rental_start_date = self.cleaned_data['arrival_date']
        instance.rental_end_date = self.cleaned_data['departure_date']
        instance.total_price = self.cleaned_data['total_price']
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Rental
        fields = ['arrival_date', 'departure_date']