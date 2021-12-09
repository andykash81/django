import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def courses_factory():
    def factory(**kwargs):
        courses = baker.make(Course, **kwargs, make_m2m=True)
        return courses
    return factory


@pytest.fixture
def students_factory():
    def factory(**kwargs):
        students = baker.prepare(Student, **kwargs)
        return students
    return factory
