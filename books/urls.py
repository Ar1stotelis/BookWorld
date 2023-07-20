from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('catalogue/', views.catalogue, name='catalogue'),
    path('add/', views.add_book, name='add_book'),
    path('delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
]
