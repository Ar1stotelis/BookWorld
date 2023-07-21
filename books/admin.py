from django.contrib import admin
from .models import Book, Category, Rating

admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Rating)
