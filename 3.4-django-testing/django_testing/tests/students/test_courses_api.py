import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_course_create(api_client, courses_factory):
    """"проверка получения 1го курса (retrieve-логика)"""
    url = reverse("courses-list")
    courses_count = 3
    courses_id = []
    for i in range(courses_count):
        course = courses_factory(name=f'Python{i}')
        courses_id.append(course.id)
    response = api_client.get(url, {'id': courses_id[1]})
    results = response.json()[0]
    assert response.status_code == HTTP_200_OK
    assert results.get('name') == 'Python1'


@pytest.mark.django_db
def test_courses_list_create(api_client, courses_factory, students_factory):
    """проверка получения списка курсов (list-логика)"""
    url = reverse("courses-list")
    st = students_factory(_quantity=10)
    courses_factory(_quantity=5, students=st)
    response = api_client.get(url)
    results = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(results) == 5


@pytest.mark.django_db
def test_filter_course_id(api_client, courses_factory):
    """проверка фильтрации списка курсов по id"""
    url = reverse("courses-list")
    courses = courses_factory(_quantity=10)
    response = api_client.get(url)
    assert response.status_code == HTTP_200_OK
    results_json = response.json()
    assert len(results_json) == 10
    results_json_id = {result['id'] for result in results_json}
    courses_id = {course.id for course in courses}
    assert results_json_id == courses_id


@pytest.mark.django_db
def test_filter_course_name(api_client, courses_factory):
    """проверка фильтрации списка курсов по name"""
    url = reverse("courses-list")
    courses = courses_factory(_quantity=10)
    response = api_client.get(url)
    assert response.status_code == HTTP_200_OK
    results_json = response.json()
    assert len(results_json) == 10
    results_json_name = {result['name'] for result in results_json}
    courses_name = {course.name for course in courses}
    assert results_json_name == courses_name


@pytest.mark.django_db
def test_filter_course_post(api_client):
    """тест успешного создания курса"""
    url = reverse("courses-list")
    request = api_client.post(url, {'name': 'django course'})
    assert request.status_code == HTTP_201_CREATED
    response = api_client.get(url, {'id': request.data['id']})
    assert response.status_code == HTTP_200_OK
    results = response.json()[0]
    assert request.data['name'] == results['name']


@pytest.mark.django_db
def test_filter_course_patch(api_client, courses_factory):
    """тест успешного обновления курса"""
    url = reverse("courses-list")
    courses = courses_factory(_quantity=10)
    courses_id = [course.id for course in courses]
    request = api_client.patch(f'{url}{courses_id[2]}/', {'name': 'django course'})
    assert request.status_code == HTTP_200_OK
    response = api_client.get(url, {'id': request.data['id']})
    assert response.status_code == HTTP_200_OK
    results = response.json()[0]
    assert request.data['name'] == results['name']


@pytest.mark.django_db
def test_filter_course_delete(api_client, courses_factory):
    """тест успешного удаления курса"""
    url = reverse("courses-list")
    courses = courses_factory(_quantity=10)
    courses_id = [course.id for course in courses]
    response = api_client.get(url, {'id': courses_id[5]})
    assert response.status_code == HTTP_200_OK
    request = api_client.delete(f'{url}{courses_id[5]}/')
    assert request.status_code == HTTP_204_NO_CONTENT
    response = api_client.get(url, {'id': courses_id[5]})
    assert response.status_code == HTTP_400_BAD_REQUEST
