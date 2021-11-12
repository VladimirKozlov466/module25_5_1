import pytest
from driver_info import driver

@pytest.fixture(autouse=True)
def testing():
    # Переходим на страницу авторизации
    driver.get('http://petfriends1.herokuapp.com/login')

    yield