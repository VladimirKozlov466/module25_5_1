from selenium.webdriver.common.by import By
from driver_info import driver
from assertpy import assert_that, soft_assertions
from user_valid_data import valid_email, valid_password

# Настраиваем неявные ожидания
driver.implicitly_wait(10)

# python3 -m pytest -v --driver Chrome --driver-path /Users/driverChrome/chromedriver /Users/vladimirkozlov/PycharmProjects/module25_5_1/tests/test_25_3.py


def test_show_my_pets():
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys(valid_email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # Находим все вебэлементы соответсвующие фотографиям питомцев
    images = driver.find_elements(By.CSS_SELECTOR, '.card-img-top')
    # Находим все вебэлементы соответсвующие именам питомцев
    names = driver.find_elements(By.CSS_SELECTOR, '.card-title')
    # Находим все вебэлементы соответсвующие виду и возрасту питомцев
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-text')

    with soft_assertions():
        for i in range(len(names)):
            # Проверяем, что у питомцев есть фотография
            assert_that(images[i].get_attribute('src')).is_not_equal_to('')
            # Проверяем, что у питомцев есть имя
            assert_that(names[i].text).is_not_empty()
            # Проверяем, что у питомцев есть порода
            assert_that(descriptions[i].text[0]).is_not_equal_to('')
            # Выделяем породу и возраст питомца
            parts = descriptions[i].text.split("\n")
            # Проверяем что у питомца есть возраст
            assert_that(parts[0].split(" ")[-2]).is_not_equal_to(',')

    driver.quit()
