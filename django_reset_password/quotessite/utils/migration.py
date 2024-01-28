# Якщо нам потрібно з бд mongodb перекинути дані на бд postgresql


import os
import django

from pymongo import MongoClient
from pymongo.server_api import ServerApi

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quotessite.settings")   # Приміняємо налаштування
django.setup()

from quotes.models import Quote, Tag, Author # noqa


client = MongoClient("mongodb+srv://STANDario:2450@clusterhomework8.z6e4gw9.mongodb.net/", server_api=ServerApi('1'))

db = client.homework_08


authors = db.authors.find()

for author in authors:
    Author.objects.get_or_create(          # Якщо в бд вже записаний цей автор, воно його повторно не буде записувати, він буде їх повертати
            fullname=author["fullname"],
            born_date=author["born_date"],
            born_location=author["born_location"],
            description=author["description"]
    )


quotes = db.quotes.find()

for quote in quotes:
    tags = []
    for tag in quote["tags"]:
        t, *_ = Tag.objects.get_or_create(name=tag)
        tags.append(t)

    exist_quote = bool(len(Quote.objects.filter(quote=quote["quote"]))) # Якщо довжина цитати = 0, то її не існує і ми її додаємо

    if not exist_quote:
        author = db.authors.find_one({"_id": quote["author"]})      # Знаходимо автора по id
        a = Author.objects.get(fullname=author["fullname"])
        q = Quote.objects.create(
            quote=quote["quote"],
            author=a               # Додаємо в цитату посилання на автора
        )
        for tag in tags:           # Додаємо в цитату теги
            q.tags.add(tag)
