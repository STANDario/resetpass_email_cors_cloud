from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from .models import Quote, Tag, Author
from .forms import AuthorForm, QuoteForm


def main(request, page=1):
    quotes = Quote.objects.all()
    per_page = 10                       # На одну сторінку може бути 10 цитат
    paginator = Paginator(list(quotes), per_page)    # Тут ми поєднуємо
    quotes_on_page = paginator.page(page)      # Вказуємо яка сторінка
    return render(request, "quotes/index.html", {"quotes": quotes_on_page}) # Передаємо в контекст


@login_required
def author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quotes:main")
        return render(request, "quotes/author.html", {"form": form})
    return render(request, "quotes/author.html", {"form": AuthorForm()})


@login_required
def quote(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()

    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.author = Author.objects.filter(fullname=request.POST.getlist('author')[0]).first()
            new_form.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_form.tags.add(tag)

            return redirect(to="quotes:main")
        return render(request, "quotes/quote.html", {"form": form, "tags": tags, "authors": authors})
    return render(request, "quotes/quote.html", {"form": QuoteForm(), "tags": tags, "authors": authors})


def author_see(request, fullname_author):
    my_author = get_object_or_404(Author, fullname=" ".join(fullname_author.split("--")))
    return render(request, "quotes/author_see.html", {"author": my_author})
