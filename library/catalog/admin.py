from django.contrib import admin

from .models import Author, Book, BookImage

classe = [Author, Book, BookImage]

for model in classe:
    admin.site.register(model)
