"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, register_converter
from django.views.generic import RedirectView

from books.converters import DateConverter
from books.views import books_view

register_converter(DateConverter, "pub_date")

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", RedirectView.as_view(pattern_name="books", permanent=False)),

    path("books/", books_view, name="books"),
    path("books/<pub_date:pub_date>/", books_view, name="books_by_date"),
]