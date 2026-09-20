"""
WSGI config for first_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "first_project.settings")

application = get_wsgi_application()


def home_view(request):

    pages = [
        {"name": "Текущее время", "url": "/current_time/"},
        {"name": "Содержимое рабочей директории", "url": "/workdir/"},
        {"name": "Админка", "url": "/admin/"},
    ]
    return render(request, "home.html", context={"pages": pages})


def time_view(request):
    now = timezone.now()
    return HttpResponse(now.strftime("%d-%m-%Y %H:%M:%S"))


def workdir_view(request):
    cwd = os.getcwd()
    items = os.listdir(cwd)

    lines = [f"Текущая директория: {cwd}", "", *items]
    return HttpResponse("<pre>" + "\n".join(lines) + "</pre>")
