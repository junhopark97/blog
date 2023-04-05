import json

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()
pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        'email': 'test@example.com',
        'password': 'password',
        'phone_number': '01000000000',
        'gender': User.GenderStatus.MALE,
    }


@pytest.fixture
def authenticated_api_client(api_client, user_data):
    User.objects.create_user(**user_data)
    response = api_client.post(reverse('token_obtain_pair'), {
        'email': user_data['email'],
        'password': user_data['password'],
    }, format='json')
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client


def test_create_user(user_data):
    user = User.objects.create_user(**user_data)
    assert user.email == user_data['email']
    assert user.check_password(user_data['password'])
    assert user.phone_number == user_data['phone_number']
    assert user.gender == user_data['gender']
    assert not user.is_staff
    assert not user.is_superuser


def test_create_superuser(user_data):
    user_data.update({
        'is_staff': True,
        'is_superuser': True,
    })
    with pytest.raises(ValueError):
        User.objects.create_superuser(**user_data)

    user_data.update({
        'is_staff': True,
        'is_superuser': True,
        'is_active': True,
    })
    user = User.objects.create_superuser(**user_data)
    assert user.email == user_data['email']
    assert user.check_password(user_data['password'])
    assert user.phone_number == user_data['phone_number']
    assert user.gender == user_data['gender']
    assert user.is_staff
    assert user.is_superuser
    assert user.is_active


def test_register(api_client, user_data):
    response = api_client.post(reverse('register'), user_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['email'] == user_data['email']
    assert 'password' not in response.data
    assert response.data['phone_number'] == user_data['phone_number']
    assert response.data['gender'] == user_data['gender']

    token = response.data['token']
    token_payload = json.loads(RefreshToken(token).payload)

    assert token_payload['email'] == user_data['email']
    assert token_payload['user_id'] == User.objects.get(email=user_data['email']).id

    response = api_client.post(reverse('register'), {
        'email': 'test@example.com',
        'password': 'password',
        'phone_number': '01000000000',
    }, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login(api_client, user_data):
    User.objects.create_user(**user_data)
    response = api_client.post(reverse('token_obtain_pair'), {
        'email': user_data['email'],
        'password': user_data['password'],
    }, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data

    refresh = response.data['refresh']
    access = response.data['access']
    verify_refresh = RefreshToken(refresh)
    verify_access = RefreshToken(access)
    assert str(verify_refresh['email']) == user_data['email']
    assert str(verify_access['email']) == user_data['email']

    response = api_client.post(reverse('token_obtain_pair'), {
        'email': user_data['email'],
        'password': 'wrongpassword',
    }, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'access' not in response.data
    assert 'refresh' not in response.data

    response = api_client.post(reverse('token_obtain_pair'), {
        'email': 'wrongemail@example.com',
        'password': user_data['password'],
    }, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'access' not in response.data
    assert 'refresh' not in response.data
