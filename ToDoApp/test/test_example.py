import pytest


def test_example():
    assert 3 == 3


def test_example_1():
    assert 5 * 5 != 4


def test_string():
    assert isinstance('hello', str)
    assert not isinstance('10', int)


def test_check_bool():
    lst = [1, 2]
    assert lst
    assert ('soccer' == 'golf') is False


def test_check_list():
    assert 6 > -1
    lst = [4, 5, 3]
    assert  4 in lst


class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


@pytest.fixture
def default_student():
    return Student('John', 'Smith', 'Marketing', 3)


def test_person_initialization(default_student):
    assert default_student.first_name == 'John'
    assert default_student.last_name == 'Smith'
    assert default_student.major == 'Marketing'
    assert default_student.years == 3