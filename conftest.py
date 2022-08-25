import os

import pytest
from django.core.files import File
from rest_framework.test import APIClient

from courses.models import CourseDay, Task
from fitness.settings import BASE_DIR
from food.models import Product, Recipe, RecipeProduct


@pytest.fixture
def user1(django_user_model):
    return django_user_model.objects.create_user(
        email="test@email.com",
        password="pass"
    )


@pytest.fixture
def user2(django_user_model):
    return django_user_model.objects.create_user(
        email="test@email2.com",
        password="pass"
    )


@pytest.fixture
def auth_client(user1):
    client = APIClient()
    response = client.post(
        path='/api/token/',
        data={
            "email": user1.email,
            "password": "pass"
        },
    )
    assert 200 == response.status_code
    client.defaults.update(HTTP_AUTHORIZATION=f'Bearer {response.data.get("access")}')
    return client


@pytest.fixture
def auth_client2(user2):
    client = APIClient()
    response = client.post(
        path='/api/token/',
        data={
            "email": user2.email,
            "password": "pass"
        },
    )
    assert 200 == response.status_code
    client.defaults.update(HTTP_AUTHORIZATION=f'Bearer {response.data.get("access")}')
    return client


@pytest.fixture
def product_1(db):
    return Product.objects.create(name="Рис")


@pytest.fixture
def product_2(db):
    return Product.objects.create(name="Греча")


@pytest.fixture
def recipe(db, product_2, product_1):
    recipe = Recipe()
    recipe.name = "Гречка с рисом"
    recipe.cooking_method = "Перемешать"
    recipe.cooking_time = 60
    recipe.calories = 100
    recipe.protein = 20
    recipe.fats = 10
    recipe.carbohydrates = 15
    recipe.image.file = File(open(os.path.join(BASE_DIR, "fixtures/recipe.jpeg")))
    recipe.save()
    RecipeProduct.objects.create(
        recipe=recipe,
        quantity=200,
        unit='гр',
        product=product_2
    )
    RecipeProduct.objects.create(
        recipe=recipe,
        quantity=200,
        unit='гр',
        product=product_1
    )
    return recipe



@pytest.fixture
def recipe2(db, product_2, product_1):
    recipe = Recipe()
    recipe.name = "Гречка с мясом"
    recipe.cooking_method = "Перемешать"
    recipe.cooking_time = 60
    recipe.calories = 100
    recipe.protein = 20
    recipe.recipe_type = 'dinner'
    recipe.fats = 10
    recipe.carbohydrates = 15
    recipe.image.file = File(open(os.path.join(BASE_DIR, "fixtures/recipe.jpeg")))
    recipe.save()
    RecipeProduct.objects.create(
        recipe=recipe,
        quantity=200,
        unit='гр',
        product=product_2
    )
    RecipeProduct.objects.create(
        recipe=recipe,
        quantity=200,
        unit='гр',
        product=product_1
    )
    return recipe


@pytest.fixture
def course_day(db):
    course_day = CourseDay.objects.create(
        number=1,
        date_of_day='2022-02-12'
    )
    Task.objects.create(
        course_day=course_day,
        name='Поесть'
    )
    return course_day


@pytest.fixture
def course_day2(db):
    course_day = CourseDay.objects.create(
        number=2,
        date_of_day='2022-02-13'
    )
    Task.objects.create(
        course_day=course_day,
        name='Попить'
    )
    return course_day


