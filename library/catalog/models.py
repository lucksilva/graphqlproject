from django.db import models

class Book(models.Model):

    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Entre a brieg description")

    class Meta:
        ordering = ['-id']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'


    def __str__(self):
        return self.title

class Author(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

class BookImage(models.Model):

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    url = models.CharField(max_length = 255)

    def __str__(self):
        return self.book.name or ""

    class Meta:

        verbose_name = 'Book Image'
        verbose_name_plural = 'Book Images'


