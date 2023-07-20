from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField()
    categories = models.ManyToManyField(Category)
    image = models.ImageField(upload_to='book_images', blank=True, null=True)

    def __str__(self):
        return self.title

    def categories_names(self):
        return ', '.join(category.name for category in self.categories.all())
