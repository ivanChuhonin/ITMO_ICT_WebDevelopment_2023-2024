from django.contrib.auth.models import Group, User
from rest_framework import serializers

from Library.models import Reader, Hall, LibraryCard, Book, BookCopy, Operation


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ReaderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reader
        fields = ['id', 'full_name', 'passport', 'address', 'birthdate', 'is_academic']


class HallSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'


class LibraryCardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LibraryCard
        fields = '__all__'


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BookCopySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BookCopy
        fields = '__all__'


class OperationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Operation
        fields = '__all__'
