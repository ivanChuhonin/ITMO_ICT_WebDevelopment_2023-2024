from django.db import models


class Reader(models.Model):
    full_name = models.CharField(max_length=50)
    passport = models.CharField(max_length=10)
    address = models.CharField(max_length=50)
    birthdate = models.DateField()
    is_academic = models.BooleanField()
    # phone_num = models.TextField(max_length=10)
    # path = models.CharField(max_length=50, default='new_hotel')

    def __str__(self):
        return self.full_name


class Hall(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.IntegerField()


class LibraryCard(models.Model):
    id_reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    date_from = models.DateField()
    date_to = models.DateField()


class Book(models.Model):
    book_name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    publishing_house = models.CharField(max_length=50)


class BookCopy(models.Model):
    CHOICES = {
        'N': 'New',
        'R': 'Regular',
        'O': 'Out of use',
    }

    condition = models.CharField(max_length=10, choices=CHOICES, default='N')
    id_book = models.ForeignKey(Book, on_delete=models.CASCADE)
    publishing_year = models.DateField()
    book_cypher = models.CharField(max_length=10)


class Operation(models.Model):
    id_book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE)
    id_library_card = models.ForeignKey(LibraryCard, on_delete=models.CASCADE)
    id_hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    date_from = models.DateField()
    date_to = models.DateField()
