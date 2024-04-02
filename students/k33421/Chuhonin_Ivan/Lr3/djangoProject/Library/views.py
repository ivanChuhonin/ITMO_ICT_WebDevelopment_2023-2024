from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets

from Library.models import Reader, LibraryCard, Hall, Book, BookCopy, Operation
from Library.serializers import GroupSerializer, UserSerializer, ReaderSerializer, HallSerializer, \
    LibraryCardSerializer, BookSerializer, BookCopySerializer, OperationSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
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
