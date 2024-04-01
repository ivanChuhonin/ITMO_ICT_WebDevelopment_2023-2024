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
def index(request):
    hotels = Hotel.objects.all()
    return render(request, "index.html", {"hotels": hotels})


def rooms(request, hotel_path: str):
    hotel = Hotel.objects.get(path=hotel_path)
    rooms_list = Room.objects.filter(id_hotel=hotel.id).all()  # .values() .all()
    return render(request, "room.html", {"rooms_list": rooms_list, "hotel": hotel})
    # return HttpResponse(f"Комнаты {hotel_path}")


def agreements(request, hotel_path: str, room_id: int):
    hotel = Hotel.objects.get(path=hotel_path)
    room = Room.objects.get(id=room_id)

    if request.method == 'POST':
        form = AgreementForm(request.POST)
        if form.is_valid():
            current_user = request.user
            guest = Guest.objects.get(id=current_user.id)
            agreement = Agreement.objects.create(id_guest=guest,
                                                 id_room=room,
                                                 date_from=form.cleaned_data['date_from'],
                                                 date_to=form.cleaned_data['date_to'])
            return redirect('/guests/profile/')
    else:
        form = AgreementForm()

    return render(request, 'agreement.html', {'form': AgreementForm(), 'hotel': hotel, 'room': room})


def review(request, agreement_id: int):
    agreement = Agreement.objects.get(id=agreement_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['id'] is None:
                review = Review.objects.create(id_agreement=agreement,
                                               comment=form.cleaned_data['comment'],
                                               rating=form.cleaned_data['rating'])
            else:
                review = Review.objects.get(id=form.cleaned_data['id'])
                review.comment = form.cleaned_data['comment']
                review.rating = form.cleaned_data['rating']
                review.save()

            return redirect('/guests/profile/')
    else:
        try:
            review_edit = Review.objects.get(id_agreement=agreement_id)
            form = ReviewForm(initial={'id': review_edit.id,
                                       'room': agreement.id_room,
                                       'date_from': agreement.date_from,
                                       'date_to': agreement.date_to,
                                       'comment': review_edit.comment,
                                       'rating': review_edit.rating,
                                       'date_review': review_edit.date_review})

        except Review.DoesNotExist:
            form = ReviewForm(initial={'room': agreement.id_room,
                                       'date_from': agreement.date_from,
                                       'date_to': agreement.date_to})
            field = form.fields['date_review']
            field.widget = field.hidden_widget()

    return render(request, 'review.html',
                  {'form': form, 'agreement_id': agreement_id})


def report(request):
    return HttpResponse("Постояльцы")


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.set_password(form.cleaned_data.get('password'))
            save_form.save()
            # messages.success(request, 'User registered successfully')
            return redirect('/guests/login/')
        else:
            return render(request, 'registration/register.html', {'form': form})

    return render(request, 'registration/register.html')


def profile(request):
    current_user = request.user
    agreement_list = Agreement.objects.filter(id_guest=current_user.id)
    return render(request, 'registration/profile.html', {'agreement_list': agreement_list})
```
Действия над классами. (создание функционала)


### `urls.py`

```python
from django.contrib import admin
from django.urls import path, include

from hotels import views

urlpatterns = [
    path("guests/register/", views.register, name="register"),
    path("guests/profile/", views.profile, name="register"),
    path("guests/", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
    path('', views.index, name='отели'),
    path('hotel/<str:hotel_path>/', views.rooms, name='номера'),
    path('hotel/<str:hotel_path>/<int:room_id>/', views.agreements, name='бронь'),
    # path('profile', views.profile, name='профиль'),
    path('guests/profile/<int:agreement_id>/', views.review, name='отзывы'),
    path('report', views.report, name='постояльцы'),
]
```