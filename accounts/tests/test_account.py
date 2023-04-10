import jwt

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient
from environ import Env

env = Env()
User = get_user_model()
pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        'email': 'test@example.com',
        'username': 'test',
        'password': 'password',
        'phone_number': '0100000000',
        'gender': User.GenderStatus.MALE,
    }


@pytest.fixture
def user_info():
    return {
        'email': 'test@example.com',
        'password': 'qwer1234!',
        'password2': 'qwer1234!',
        'gender': User.GenderStatus.MALE,
        'username': 'test',
        'phone_number': '01000000000',
    }


def test_create_user(user_data):
    user = User.objects.create_user(**user_data)
    assert user.email == user_data['email']
    assert user.check_password(user_data['password'])
    assert user.username == user_data['username']
    assert user.phone_number == user_data['phone_number']
    assert user.gender == user_data['gender']
    assert not user.is_staff
    assert not user.is_superuser


def test_register(api_client, user_info):
    response = api_client.post(reverse('register'), user_info, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['email'] == user_info['email']
    assert 'password' not in response.data
    assert response.data['phone_number'] == user_info['phone_number']
    assert response.data['gender'] == user_info['gender']

    access = response.data['token']['access']
    verify_access = jwt.decode(access, env('SECRET_KEY'), algorithms=['HS256'])
    refresh = response.data['token']['refresh']
    verify_refresh = jwt.decode(refresh, env('SECRET_KEY'), algorithms=['HS256'])

    assert verify_access.get('email') == user_info['email']
    assert verify_access.get('user_id') == str(User.objects.get(email=user_info['email']).id)
    assert verify_refresh.get('email') == user_info['email']
    assert verify_refresh.get('user_id') == str(User.objects.get(email=user_info['email']).id)

    # Updated assertion to expect a 400 status code
    response = api_client.post(reverse('register'), {
        'email': 'test@example.com',
        'password': 'password',
        'phone_number': '01000000000',
    }, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login(api_client, user_data):
    User.objects.create_user(**user_data)
    response = api_client.post(reverse('login'), {
        'email': user_data['email'],
        'password': user_data['password'],
    }, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'access_token' in response.data['token']
    assert 'refresh_token' in response.data['token']

    access = response.data['token']['access_token']
    verify_access = jwt.decode(access, env('SECRET_KEY'), algorithms=['HS256'])
    refresh = response.data['token']['refresh_token']
    verify_refresh = jwt.decode(refresh, env('SECRET_KEY'), algorithms=['HS256'])

    assert verify_access.get('email') == user_data['email']
    assert verify_refresh.get('email') == user_data['email']

    response = api_client.post(reverse('login'), {
        'email': user_data['email'],
        'password': 'wrongpassword',
    }, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'token' not in response.data

    response = api_client.post(reverse('login'), {
        'email': 'wrongemail@example.com',
        'password': user_data['password'],
    }, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'token' not in response.data
