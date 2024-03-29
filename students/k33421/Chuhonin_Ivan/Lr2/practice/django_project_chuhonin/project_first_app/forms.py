from django import forms
from .models import Driver, Car


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['first_name', 'last_name', 'birth_date'] # 'username', 'password',
        labels = {
            # 'username': 'login',
            # 'password': 'password',
            'first_name': 'name',
            'last_name': 'surname',
            'birth_date': 'birthdate'
        }


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['car_number', 'brand', 'model', 'color']
        labels = {
            'car_number': 'car_number',
            'brand': 'brand',
            'model': 'model',
            'color': 'color',
        }