import pytest
from rest_framework.test import APIClient
from rest_framework import status
from model_bakery import baker
from students.models import Course, Student


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(**kwargs):
        return baker.make(Course, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(**kwargs):
        return baker.make(Student, **kwargs)

    return factory


import pytest


@pytest.mark.django_db
def test_retrieve_first_course(api_client, course_factory):
    # Создаем курс с помощью фабрики
    course = course_factory()

    # Выполняем GET-запрос для получения первого курса
    response = api_client.get(f"/api/v1/courses/{course.id}/")

    # Проверяем, что вернулся статус-код 200
    assert response.status_code == 200

    # Проверяем, что вернулся ожидаемый JSON-объект
    assert response.json() == {
        "id": course.id,
        "name": course.name,
        "students": [],
    }


@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    # Создаем несколько курсов с помощью фабрики
    course1 = course_factory()
    course2 = course_factory()

    # Выполняем GET-запрос для получения списка курсов
    response = api_client.get("/api/v1/courses/")

    # Проверяем, что вернулся статус-код 200
    assert response.status_code == 200

    # Проверяем, что вернулся список всех курсов
    assert response.json() == [
        {
            "id": course1.id,
            "name": course1.name,
            "students": [],
        },
        {
            "id": course2.id,
            "name": course2.name,
            "students": [],
        },
    ]


@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    # Создаем 2 курса с разными id
    course_factory(id=1, name="Python")
    course_factory(id=2, name="Java")

    # Отправляем GET запрос с параметром id, который должен вернуть только курс с id=1
    response = api_client.get("/api/v1/courses/", data={"id": 1})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["id"] == 1
    assert response.data[0]["name"] == "Python"


@pytest.mark.django_db
def test_create_course(api_client):
    # Отправляем POST запрос на создание курса
    data = {"name": "C#"}
    response = api_client.post("/api/v1/courses/", data)

    assert response.status_code == status.HTTP_201_CREATED
    assert Course.objects.filter(name="C#").exists()


@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    # Создаем курс
    course = course_factory(name="Python")

    # Отправляем PUT запрос на обновление курса с новым именем
    data = {"name": "Django"}
    response = api_client.put(f"/api/v1/courses/{course.id}/", data)
    assert response.status_code == status.HTTP_200_OK
    assert Course.objects.filter(name="Django").exists()


@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    # Создаем курс
    course = course_factory(name="Python")

    # Отправляем DELETE запрос на удаление курса
    response = api_client.delete(f"/api/v1/courses/{course.id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Course.objects.filter(id=course.id).exists()
