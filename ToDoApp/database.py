from sqlalchemy import create_engine #Создает объект подключения к базе данных.
from sqlalchemy.orm import sessionmaker #Создает фабрику для генерации сессий, которые используются для взаимодействия с базой данных.
from sqlalchemy.ext.declarative import declarative_base #Используется для определения базового класса, от которого будут наследоваться все модели базы данных.

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:root1847@localhost/TodoApplicationDatabase'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()