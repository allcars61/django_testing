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


# Проверка получения списка курсов
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


# Проверка фильтрации списка курсов по имени
@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    # Создаем несколько курсов с помощью фабрики
    course1 = course_factory(name="Python")
    course2 = course_factory(name="Java")

    # Выполняем GET-запрос для получения списка курсов с фильтром по имени
    response = api_client.get("/api/v1/courses/?name=Python")

    # Проверяем, что вернулся статус-код 200
    assert response.status_code == 200

    # Проверяем, что вернулся список курсов с фильтром по имени
    assert response.json() == [
        {
            "id": course1.id,
            "name": course1.name,
            "students": [],
        },
    ]
