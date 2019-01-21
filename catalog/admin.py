from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language
# Register your models here.
#admin.site.register(Book)
class BooksInstanceInline(admin.TabularInline):
    extra = 0
    model = BookInstance
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    search_fields = ('title', )
    list_filter = ('title', 'author')
    inlines = [BooksInstanceInline]

# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    search_fields = ('status',)
    list_filter = ('status', 'due_back')
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )
#admin.site.register(BookInstance)
admin.site.register(Language)
