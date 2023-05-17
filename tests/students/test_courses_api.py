import pytest

@pytest.mark.django_db
def test_retrieve_first_course(api_client, course_factory):
    # Создаем курс с помощью фабрики
    course = course_factory()

    # Выполняем GET-запрос для�получения первого курса
    response = api_client.get(f'/api/v1/courses/{course.id}/')

    # Проверяем, что вернулся статус-код 200
    assert response.status_code == 200

    # Проверяем, что вернулся ожидаемый JSON-объект
    assert response.json() == {
        'id': course.id,
        'name': course.name,
        'students': [],
    }