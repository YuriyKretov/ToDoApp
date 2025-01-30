from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ToDoApp.database import Base
from ToDoApp.main import app
from fastapi.testclient import TestClient
from ..models import Todos, Users
import pytest
from ..routers.users import bcrypt_context

SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False,
                                   autoflush=False,
                                   bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {'username': 'jurgen', 'id': 1, 'role': 'admin'}


client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todos(title='learn Golang',
                 description='To get one more option for backend',
                 priority=2,
                 complete=False,
                 owner_id=1)

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield db
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        username= 'jurgen',
        email='jurgen@email.com',
        first_name='jurgen',
        last_name= 'klopp',
        hashed_password=bcrypt_context.hash('1234'),
        role='admin',
        phone_number='1234'
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()

