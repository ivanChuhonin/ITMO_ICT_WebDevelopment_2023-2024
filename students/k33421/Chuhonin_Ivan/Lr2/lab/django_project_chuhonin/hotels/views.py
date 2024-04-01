from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader, Context, Template

from hotels.forms import SignUpForm, AgreementForm, ReviewForm
from hotels.models import Hotel, Room, Agreement, Guest, Review


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
