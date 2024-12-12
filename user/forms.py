from django import forms
from django.core.exceptions import ValidationError

from user.models import User

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class UserEditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'date_of_birth', 'avatar']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'email': forms.EmailInput(attrs={
                'class': INPUT_CLASSES
            }),
            'first_name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'last_name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'date_of_birth': forms.DateInput(attrs=
            {
                'class': INPUT_CLASSES,
                'type': 'date'
            }),
            'avatar': forms.ClearableFileInput(attrs=
            {
                'class': INPUT_CLASSES
            }),
        }
    def clean_birth_date(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth:
            import datetime
            age = (datetime.date.today() - date_of_birth).days // 365
            if age < 18:
                raise ValidationError("Age of user shouldn`t be under 18.")
        return date_of_birth
