from .utils import *
from ..models import Users
from fastapi import status
from ..routers.users import get_db, get_current_user


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get('/user')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'jurgen'
    assert response.json()['email'] == 'jurgen@email.com'
    assert response.json()['first_name'] == 'jurgen'
    assert response.json()['last_name'] == 'klopp'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '1234'


def test_change_password_success(test_user):
    response = client.put('/user/password', json={'password': '1234', 'new_password': 'new_password'})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid(test_user):
    response = client.put('/user/password', json={'password': 'wrong password', 'new_password': 'new_password'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Error on password change.'}


def test_change_phone_number_success(test_user):
    response = client.put('/user/phone_number/123456')
    assert response.status_code == status.HTTP_204_NO_CONTENT




