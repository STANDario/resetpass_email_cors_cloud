# Робимо цей файл щоб могли в index.html виводити авторів, а не їх id

from django import template


register = template.Library()


def get_author(aut):
    author = aut.fullname
    return author


register.filter('author', get_author)


def get_tags(quote):
    return quote.tags.all()   # Щоб дістати з ManyToManyField треба додавати в кінці ".all()"


register.filter('tags', get_tags)


def new_url(name_author):
    name_author = name_author.split(" ")
    result = "--".join(name_author)
    return result


register.filter('url', new_url)
