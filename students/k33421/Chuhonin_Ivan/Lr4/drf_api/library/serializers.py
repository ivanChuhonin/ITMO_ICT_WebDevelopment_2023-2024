from django.contrib.auth.models import User
from rest_framework import serializers

from library.models import Reader, Hall, LibraryCard, Book, BookCopy, Operation


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'password', 'email']
        extra_kwargs = {"id": {"read_only": True}, "password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data['email']
        instance.username = validated_data['username']
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'password', 'email']
        extra_kwargs = {"id": {"read_only": True}, "password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        return user


class ReaderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reader
        fields = ['id', 'full_name', 'passport', 'address', 'birthdate', 'is_academic']


class HallSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hall
        fields = ['id', 'name', 'capacity']


class LibraryCardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LibraryCard
        fields = '__all__'


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'book_name', 'author', 'area', 'publishing_house']
        extra_kwargs = {"id": {"read_only": True}}


class BookCopySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BookCopy
        fields = '__all__'


class OperationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Operation
        fields = ['id_book', 'id_book_copy', 'id_library_card', 'id_hall', 'date_from']
