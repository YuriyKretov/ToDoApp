from fastapi import status
from ToDoApp.routers.todos import get_db
from ToDoApp.routers.auth import get_current_user
from .utils import *


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authenticated(test_todo):
    response = client.get('/todos/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'id': 1,
                                'title': 'learn Golang',
                                'description': 'To get one more option for backend',
                                'priority': 2,
                                'complete': False,
                                'owner_id': 1}]


def test_read_one_authenticated(test_todo):
    response = client.get('/todos/todo/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'id': 1,
                                'title': 'learn Golang',
                                'description': 'To get one more option for backend',
                                'priority': 2,
                                'complete': False,
                                'owner_id': 1}


def test_read_one_authenticated_not_found(test_todo):
    response = client.get('/todos/todo/1111')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo Not Found'}


def test_create_todo(test_todo):
    request_data = {'title': 'learn calculus',
                    'description': 'to improve own ml models',
                    'priority': 2,
                    'complete': False}

    response = client.post('/todos/todo/', json=request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')


def test_update_todo(test_todo):
    request_data = {
        'title': 'learn linear algebra',
        'description': 'to master matrix multiplication',
        'priority': 2,
        'complete': False
    }

    response = client.put('/todos/todo/1', json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')


def test_update_todo_not_found(test_todo):
    request_data = {
        'title': 'learn linear algebra',
        'description': 'to master matrix multiplication',
        'priority': 2,
        'complete': False
    }

    response = client.put('/todos/todo/1111', json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}


def test_delete_todo(test_todo):
    response = client.delete('/todos/todo/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_todo_not_found(test_todo):
    response = client.delete('/todos/todo/11111')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}