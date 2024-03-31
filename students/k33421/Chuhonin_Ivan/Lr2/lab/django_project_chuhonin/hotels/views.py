from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader, Context, Template

from hotels.forms import SignUpForm
from hotels.models import Hotel, Room


def index(request):
    hotels = Hotel.objects.all()
    return render(request, "index.html", {"hotels": hotels})


def rooms(request, hotel_path: str):
    hotel = Hotel.objects.filter(path=hotel_path).get()
    rooms_list = Room.objects.filter(id_hotel=hotel.id).all()  # .values() .all()
    return render(request, "room.html", {"rooms_list": rooms_list, "hotel": hotel})
    # return HttpResponse(f"Комнаты {hotel_path}")


def agreements(request):
    return HttpResponse("Бронь")


def review(request):
    # reviews = Review.objects.all()
    # return render(request, "review.html", {"reviews": reviews})
    return HttpResponse("Отзыв")


def report(request):
    return HttpResponse("Постояльцы")


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            save_form = form.save(commit = False)
            save_form.set_password(form.cleaned_data.get('password'))
            save_form.save()
            # messages.success(request, 'User registered successfully')
            return redirect('/guests/login/')
        else:
            return render(request, 'registration/register.html', {'form':form})

    return render(request, 'registration/register.html')


def profile(request):
    return render(request, 'registration/profile.html')
