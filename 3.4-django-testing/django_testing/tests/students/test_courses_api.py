import pytest
from django.urls import reverse
from rest_framework import status

from students.models import Course


@pytest.mark.django_db
def test_retrieve_course(api_client, course_factory):
    # Создаем курс
    course = course_factory()

    # Формируем URL
    url = reverse("courses-detail", args=[course.id])

    # Отправляем GET-запрос
    response = api_client.get(url)

    # Проверяем статус ответа
    assert response.status_code == status.HTTP_200_OK

    # Проверяем, что получили нужный курс
    assert response.data["id"] == course.id
    assert response.data["name"] == course.name


@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    # Создаем несколько курсов
    courses = course_factory(_quantity=5)

    # Формируем URL
    url = reverse("courses-list")

    # Отправляем GET-запрос
    response = api_client.get(url)

    # Проверяем статус ответа
    assert response.status_code == status.HTTP_200_OK

    # Проверяем количество курсов
    assert len(response.data) == len(courses)

    # Проверяем ID полученных курсов
    course_ids = {course.id for course in courses}
    response_ids = {course["id"] for course in response.data}

    assert response_ids == course_ids


@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    # Создаем несколько курсов
    courses = course_factory(_quantity=5)

    # Выбираем один курс
    course = courses[0]

    # Формируем URL
    url = reverse("courses-list")

    # Отправляем запрос с фильтром по ID
    response = api_client.get(url, data={"id": course.id})

    # Проверяем статус ответа
    assert response.status_code == status.HTTP_200_OK

    # Проверяем количество найденных курсов
    assert len(response.data) == 1

    # Проверяем ID курса
    assert response.data[0]["id"] == course.id


@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    # Создаем курсы
    course_factory(name="Python")
    course_factory(name="Java")
    course_factory(name="Django")

    # Формируем URL
    url = reverse("courses-list")

    # Отправляем запрос с фильтром по названию
    response = api_client.get(url, data={"name": "Python"})

    # Проверяем статус ответа
    assert response.status_code == status.HTTP_200_OK

    # Проверяем количество найденных курсов
    assert len(response.data) == 1

    # Проверяем название курса
    assert response.data[0]["name"] == "Python"


@pytest.mark.django_db
def test_create_course(api_client):
    # Данные нового курса
    data = {
        "name": "Python для начинающих",
        "students": [],
    }

    # Формируем URL
    url = reverse("courses-list")

    # Отправляем POST-запрос
    response = api_client.post(url, data=data, format="json")

    # Проверяем статус ответа
    assert response.status_code == status.HTTP_201_CREATED

    # Проверяем название созданного курса
    assert response.data["name"] == data["name"]

    # Проверяем наличие курса в базе данных
    assert Course.objects.filter(
        name=data["name"]
    ).exists()


@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    # Создаем курс
    course = course_factory(name="Старое название")

    # Новые данные
    data = {
        "name": "Новое название",
        "students": [],
    }

    # Формируем URL
    url = reverse("courses-detail", args=[course.id])

    # Отправляем PUT-запрос
    response = api_client.put(url, data=data, format="json")

    # Проверяем статус ответа
    assert response.status_code == status.HTTP_200_OK

    # Обновляем объект из базы данных
    course.refresh_from_db()

    # Проверяем новое название
    assert course.name == data["name"]
    assert response.data["name"] == data["name"]


@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    # Создаем курс
    course = course_factory()

    # Формируем URL
    url = reverse("courses-detail", args=[course.id])

    # Отправляем DELETE-запрос
    response = api_client.delete(url)

    # Проверяем статус ответа
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Проверяем, что курс удален из базы
    assert not Course.objects.filter(id=course.id).exists()