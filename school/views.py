from django.shortcuts import render
from .models import Student


def students_list(request):
    template = 'school/students_list.html'
    ordering = 'group'

    students = Student.objects.prefetch_related('teachers').order_by(ordering)

    return render(request, template, {'object_list': students})