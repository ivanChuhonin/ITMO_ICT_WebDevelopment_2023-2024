# Лабораторная работа №2

## Цель
Овладеть практическими навыками и умениями реализации web-сервисов
средствами Django 2.2.

## Описание Задачи

Реализовать сайт используя фреймворк Django 3 и СУБД PostgreSQL*, в
соответствии с вариантом задания лабораторной работы.

## Вариант работы - 1 (список отелей)
Необходимо учитывать название отеля, владельца отеля, адрес, описание, типы
номеров, стоимость, вместимость, удобства.
Необходимо реализовать следующий функционал:

*  Регистрация новых пользователей.

*  Просмотр и резервирование номеров. Пользователь должен иметь
возможность редактирования и удаления своих резервирований.

*  Написание отзывов к номерам. При добавлении комментариев, должны
сохраняться период проживания, текст комментария, рейтинг (1-10),
информация о комментаторе.

*  Администратор должен иметь возможность заселить пользователя в отель и
выселить из отеля средствами Django-admin.

*  В клиентской части должна формироваться таблица, отображающая
постояльцев отеля за последний месяц.

## UML модель
Место для модели


## Реализация 

### `Models.py`

```python
from django.db import models
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
    id_room = models.ForeignKey('Room', on_delete=models.CASCADE)
    id_guest = models.ForeignKey('Guest', on_delete=models.CASCADE)
    date_from = models.DateTimeField(auto_now_add=True)
    date_to = models.DateTimeField()


class Review(models.Model):
    id_agreement = models.ForeignKey('Agreement', on_delete=models.CASCADE)
    date_review = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
```

В указанном фрагменте кода описывается реализация классов, находящихся в uml диаграмме и необходимых далее.
Из интересного здесь есть переменная с выборным значением, заданная с помощью CHOISES, также есть переменные с указанным возможным промежутком значений.
Foreign keys заданы, primary keys создаются автоматически.

### `Views.py`

```python
from django.urls import path
from django.contrib import admin
urlpatterns = [
    path("guests/register/", views.register, name="register"),
    path("guests/profile/", views.profile, name="register"),
    path("guests/", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
    path('', views.index, name='отели'),
    path('hotel/<str:hotel_path>/', views.rooms, name='номера'),
    path('agreements', views.agreements, name='бронь'),
    # path('profile', views.profile, name='профиль'),
    path('review', views.review, name='отзывы'),
    path('report', views.report, name='постояльцы'),
]
```
Сервер