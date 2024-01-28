from django.forms import CharField, TextInput, ModelForm, Textarea

from .models import Author, Quote


class AuthorForm(ModelForm):
    fullname = CharField(max_length=50, required=True, widget=TextInput(attrs={"class": "form-control"}))
    born_date = CharField(max_length=50, widget=TextInput(attrs={"class": "form-control"}))
    born_location = CharField(max_length=150, widget=TextInput(attrs={"class": "form-control"}))
    description = CharField(widget=Textarea(attrs={"class": "form-control"}))

    class Meta:
        model = Author
        fields = ["fullname", "born_date", "born_location", "description"]


class QuoteForm(ModelForm):
    quote = CharField(required=True, widget=Textarea(attrs={"class": "form-control", "placeholder": "Enter quote"}))

    class Meta:
        model = Quote
        fields = ["quote"]
        exclude = ["tags", "author"]
