from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('catalogue/', views.catalogue, name='catalogue'),
    path('add/', views.add_book, name='add_book'),
    path('books/delete/<int:pk>/', views.delete_book, name='delete_book'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('book/delete_comment/', views.delete_comment, name='delete_comment'),
    path('add_category/', views.add_category, name='add_category'),
    path('delete_category/', views.delete_category, name='delete_category'),

]
