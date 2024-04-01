from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class Guest(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    is_verified = models.BooleanField(default=False)


class Hotel(models.Model):
    name = models.CharField(max_length=50)
    owner_name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    description = models.TextField()
    path = models.CharField(max_length=50, default='newhotel')

    def __str__(self):
        return self.name


class Room(models.Model):

    CHOICES = {
        'L': 'Люкс',
        'S': 'Стандарт',
        # ('single', 'single'),
        # ('double', 'double'),
        # ('twin', 'twin'),
        # ('triple', 'triple'),
    }

    room_type = models.CharField(max_length=10, choices=CHOICES, default='S')
    id_hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    facilities = models.TextField()
    price = models.IntegerField()
    capacity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    room_no = models.CharField(max_length=50, default='1')

    def __str__(self):
        return f'{self.CHOICES[self.room_type]} для {self.capacity} гостей'


class Agreement(models.Model):
    id_room = models.ForeignKey(Room, on_delete=models.CASCADE)
    id_guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    date_from = models.DateField()
    date_to = models.DateField()

    def __str__(self):
        return f'{self.id_room} по адресу {self.id_room.id_hotel.address}'


class Review(models.Model):
    id_agreement = models.ForeignKey(Agreement, on_delete=models.CASCADE)
    date_review = models.DateField(auto_now_add=True)
    comment = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
