from django.db import models
from django.urls import reverse  # To generate URLS by reversing URL patterns
import uuid  # Required for unique book instances
from datetime import date
from django import forms

from django.contrib.auth.models import User  # Required to assign User as a borrower

class Genre(models.Model):
    """Model representing a book genre (e.g. Science Fiction, Non Fiction)."""
    name = models.CharField(
        'Название',
        max_length=200,
        help_text="Введите жанр книги (например Фантастика, Приключения и т.д.)"
        )
    class Meta:
        verbose_name="Жанр"
        verbose_name_plural="Жанры"

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField('Название',max_length=200, help_text="Введите язык книги")
    class Meta:
        verbose_name="Язык"
        verbose_name_plural="Языки"
    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField('Оглавление',max_length=200)
    author = models.ForeignKey('Author',verbose_name='Автор', on_delete=models.SET_NULL, null=True)
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in file.
    summary = models.TextField('Описание',max_length=1000, help_text="Введите короткое описание книги")
    isbn = models.CharField('ISBN', max_length=13, help_text='13 символьный <a href="https://www.isbn-international.org/content/what-isbn">ISBN</a>')
    genre = models.ManyToManyField(Genre,verbose_name='Жанр', help_text="Выберите жанр книги")
    # ManyToManyField used because a genre can contain many books and a Book can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    language = models.ForeignKey('Language',verbose_name='Язык', on_delete=models.SET_NULL, null=True)

    def display_genre(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([genre.name for genre in self.genre.all()[:6]])

    display_genre.short_description = 'Жанр'

    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return reverse('book-detail', args=[str(self.id)])
    class Meta:
        verbose_name="Книга"
        verbose_name_plural="Книги"
    def __str__(self):
        """String for representing the Model object."""
        return self.title


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID для этой книги в библиотеке")
    book = models.ForeignKey('Book',verbose_name='Книга', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200,verbose_name='Картинка')
    due_back = models.DateField(null=True, blank=True,verbose_name='Дата возврата')
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,verbose_name='Абонент')

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    LOAN_STATUS = (
        ('d', 'На содержании'),
        ('o', 'Выдана'),
        ('a', 'Доступна'),
        ('r', 'Зарезервирована'),
    )

    status = models.CharField(
        verbose_name='Статус',
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='d',
        help_text='Доступность книги')


    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Книга возвращена"),)
        verbose_name = "Экземпляр книги"
        verbose_name_plural = "Экземпляры книг"

    def __str__(self):
        """String for representing the Model object."""
        return '{0} [{2}] ({1})'.format(self.book.title,  self.id, self.status)


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100,verbose_name='Имя')
    last_name = models.CharField(max_length=100,verbose_name='Фамилия')
    date_of_birth = models.DateField(null=True, blank=True,verbose_name='Дата рождения')
    date_of_death = models.DateField('умер', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0}, {1}'.format(self.last_name, self.first_name)


