from django.contrib import admin

# Register your models here.


from .models import *



class BookUser(admin.ModelAdmin):
    list_display = ['title', 'isbn', 'page_count', 'published_date', 'image']

admin.site.register(Book, BookUser)