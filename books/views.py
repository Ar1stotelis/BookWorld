import json
from json import JSONDecodeError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
from .models import Book, Rating, Category
from .forms import BookForm, BookFilterForm, RatingForm
from django.http import JsonResponse
from django.contrib import messages


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
    categories = Category.objects.all()  # Fetch categories
    return render(request, 'books/add_book.html', {'form': form, 'categories': categories})  # Add categories to context

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.image:  # Check if the image exists before trying to delete it
        book.image.delete(save=False)
    book.delete()
    return redirect('books:catalogue')


def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    ratings = Rating.objects.filter(book=book)

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = Rating(
                user=request.user,
                book=book,
                rating=form.cleaned_data['rating'],
                comment=form.cleaned_data.get('comment', '')
            )

            rating.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'username': request.user.username,
                    'rating': rating.rating,
                    'comment': rating.comment,
                    'ratingId': rating.id,  # Add this line
                })
            return redirect('books:book_detail', book_id=book_id)

    else:
        form = RatingForm()

    return render(request, 'books/book_detail.html', {'book': book, 'ratings': ratings, 'form': form})


@login_required
@require_http_methods(["DELETE"])
def delete_comment(request):
    if request.body:  # check if body is not empty
        try:
            data = json.loads(request.body)
            comment_id = data.get('rating_id')
            comment = Rating.objects.get(id=comment_id)
            if request.user == comment.user or request.user.is_staff:
                comment.delete()
                return JsonResponse({'status': 'success'}, status=200)
            else:
                return JsonResponse({'status': 'fail', 'message': 'Not authorized'}, status=403)
        except JSONDecodeError:
            return JsonResponse({'status': 'fail', 'message': 'Invalid data'}, status=400)
    else:
        return JsonResponse({'status': 'fail', 'message': 'No data provided'}, status=400)

@login_required
@user_passes_test(lambda u: u.is_staff)
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            category, created = Category.objects.get_or_create(name=name)
            if created:
                return JsonResponse({'status': 'success'}, status=201)
            else:
                return JsonResponse({'error': 'Category already exists'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid category name'}, status=400)

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_category(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                if Book.objects.filter(categories__id=category_id).exists():
                    return JsonResponse({'error': 'Category is being used by a book and cannot be deleted'}, status=400)
                category.delete()
                return JsonResponse({'status': 'success'}, status=200)
            except Category.DoesNotExist:
                return JsonResponse({'error': 'Category does not exist'}, status=404)
        else:
            return JsonResponse({'error': 'Invalid category id'}, status=400)
