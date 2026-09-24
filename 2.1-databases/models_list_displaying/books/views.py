from django.http import Http404
from django.shortcuts import render

from books.models import Book


def books_view(request, pub_date=None):
    template = "books/books_list.html"

    books = Book.objects.all().order_by("pub_date", "name")

    dates = list(
        Book.objects.values_list("pub_date", flat=True).distinct().order_by("pub_date")
    )

    prev_date = None
    next_date = None

    if pub_date is not None:
        if pub_date not in dates:
            raise Http404("No books for this date")

        books = books.filter(pub_date=pub_date).order_by("name")

        idx = dates.index(pub_date)
        if idx > 0:
            prev_date = dates[idx - 1]
        if idx < len(dates) - 1:
            next_date = dates[idx + 1]

    context = {
        "books": books,
        "prev_date": prev_date,
        "next_date": next_date,
    }
    return render(request, template, context)