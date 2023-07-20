from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Book, Category
from .forms import BookForm, BookFilterForm

def catalogue(request):
    filter_form = BookFilterForm(request.GET)
    books = Book.objects.all()

    if filter_form.is_valid():
        query = filter_form.cleaned_data.get('query')
        category = filter_form.cleaned_data.get('category')

        if query:
            books = books.filter(title__icontains=query)
        if category:
            books = books.filter(categories__name=category.name)

    return render(request, 'books/catalogue.html', {'books': books, 'filter_form': filter_form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            return redirect('books:catalogue')
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    return redirect('books:catalogue')

def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'books/book_detail.html', {'book': book})
