from django.urls import path

from . import views


app_name = "quotes"

urlpatterns = [
    path("", views.main, name="main"),
    path("page/<int:page>", views.main, name="root_paginate"), # Якщо інша сторінка, повертає ту ж функцію
    path("add_author", views.author, name="add_author"),
    path("add_quote", views.quote, name="add_quote"),
    path("author/<str:fullname_author>", views.author_see, name="author_see")   # Щоб використовувати ім'я в url, воно має бути унікальним в models.py
]
