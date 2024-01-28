from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=40, null=False, unique=True)


class Author(models.Model):
    fullname = models.CharField(max_length=50, unique=True)
    born_date = models.CharField(max_length=50)
    born_location = models.CharField(max_length=150)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Quote(models.Model):
    quote = models.TextField()
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=None, null=True) # Може бути пустим
    created_at = models.DateTimeField(auto_now_add=True)

