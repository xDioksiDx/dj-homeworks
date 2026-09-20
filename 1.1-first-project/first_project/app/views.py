import os
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render


def home_view(request):
    pages = [
        {"title": "Главная страница", "url": "/"},
        {"title": "Показать текущее время", "url": "/current_time/"},
        {"title": "Показать содержимое рабочей директории", "url": "/workdir/"},
    ]
    return render(request, "home.html", {"pages": pages})


def time_view(request):
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    return HttpResponse(f"Текущее время: {now}")


def workdir_view(request):
    cwd = os.getcwd()
    files = os.listdir(cwd)

    content = "Содержимое рабочей директории:\n\n" + "\n".join(files)
    return HttpResponse(f"<pre>{content}</pre>")