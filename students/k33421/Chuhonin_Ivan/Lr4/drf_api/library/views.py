# from rest_framework.views import APIView
import datetime
0
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token

from library.models import Reader, LibraryCard, Hall, Book, BookCopy, Operation
from library.serializers import UserSerializer, ReaderSerializer, HallSerializer, \
    LibraryCardSerializer, BookSerializer, BookCopySerializer, OperationSerializer, RegistrationSerializer


@api_view(['GET'])
def get_read(request):
    reader = Reader.objects.all()
    return Response(
        {
            "reader": {
                "id": reader.id,
                "username": reader.full_name,
                "passport": reader.passport,
            }
        })


def edit_profile(request):
    temp = Reader.objects.all()
    serializer = ReaderSerializer(temp, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def userprofile(request):
    user = request.user
    reader = Reader.objects.get(user=user)
    return Response(
        {
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            "reader": {
                "id": reader.id,
                "full_name": reader.full_name,
                "address": reader.address,
                "passport": reader.passport,
                "birthdate": reader.birthdate,
                "is_academic": reader.is_academic,
            }
        })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def save_userprofile(request):
    user = request.user
    reader_serializer = ReaderSerializer(data=request.data)
    if not reader_serializer.is_valid():
        return Response(
            {
                "error": "данные содержат ошибку",
                "status": f"{status.HTTP_406_NOT_ACCEPTABLE} ERROR",
            })
    edit_reader = Reader.objects.get(user=request.user)
    edit_reader.full_name = reader_serializer.data["full_name"]
    edit_reader.address = reader_serializer.data["address"]
    edit_reader.passport = reader_serializer.data["passport"]
    edit_reader.birthdate = reader_serializer.data["birthdate"]
    edit_reader.is_academic = reader_serializer.data["is_academic"]
    edit_reader.save()
    return Response(
        {
            "success": "пользователь coхранен",
            "status": f"{status.HTTP_200_OK} OK",
        })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def registration(request):
    """Handles post request logic"""
    registration_serializer = RegistrationSerializer(data=request.data)
    if not registration_serializer.is_valid():
        return Response(
            {
                "error": "данные содержат ошибку",
                "status": f"{status.HTTP_406_NOT_ACCEPTABLE} ERROR",
            })
    existed = User.objects.filter(username=registration_serializer.data['username'])
    if len(existed) > 0:
        return Response(
            {
                "error": "пользователь уже существует",
                "status": f"{status.HTTP_226_IM_USED} ERROR",
            })

    user = registration_serializer.save()
    user.save()

    reader = Reader.objects.create(
        user=user,
        full_name='',
        passport='0000000000',
        address='',
        birthdate=datetime.date(1901, 1, 1),
        is_academic=False)
    reader.save()

    # Generate tokens for existing users
    try:
        token = Token.objects.get(user_id=user.id)
    except Token.DoesNotExist:
        token = Token.objects.create(user=user)

    return Response(
        {
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            "status": {
                "message": "User created",
                "code": f"{status.HTTP_200_OK} OK",
            },
            "token": token.key,
        })


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReaderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Reader.objects.all().order_by('full_name')
    serializer_class = ReaderSerializer


class HallViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Hall.objects.all().order_by('name')
    serializer_class = HallSerializer
    permission_classes = [permissions.AllowAny]


class LibraryCardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = LibraryCard.objects.all()  # .order_by('date_from')
    serializer_class = LibraryCardSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Book.objects.all().order_by('book_name')
    serializer_class = BookSerializer


class BookCopyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = BookCopy.objects.all().order_by('publishing_year')
    serializer_class = BookCopySerializer


class OperationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Operation.objects.all().order_by('date_from')
    serializer_class = OperationSerializer
