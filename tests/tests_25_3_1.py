from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from driver_info import driver
from user_valid_data import valid_email, valid_password
from assertpy import assert_that, soft_assertions

# Строка для запуска теста
# python3 -m pytest -v --driver Chrome --driver-path /Users/driverChrome/chromedriver /Users/vladimirkozlov/PycharmProjects/module25_5_1/tests/tests_25_3_1.py


# Настраиваем явное ожидание
wait = WebDriverWait(driver, 5)


def test_all_my_pets_presents():
    """Проверяем что количество питомцев из статистики пользователя соответствут отображаемым питомцам"""
    # Вводим email пользователя
    driver.find_element(By.ID, 'email').send_keys(valid_email)
    # Вводим пароль пользователя
    driver.find_element(By.ID, 'pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()
    # Нажимаем кнопку "Мои питомцы" для вызова списка питомцев пользователя
    wait.until(EC.visibility_of_element_located((By.XPATH, '//a[contains(text(), "Мои питомцы")]'))).click()
    # Выбираем всех питомцев пользователя по локатору для кнопки удаления питомца
    locator_for_all_my_pets = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//td[@class="smart_cell"]')))
    # Находим информацию о статистике пользователя, достаем из нее текст и разбиваем с переносом строки
    user_statistic_info = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split("\n")
    # Достаем строку с индексом "1" в которой находится количество питомцев пользователя и разбиваем пробелом
    user_statistics_pets = user_statistic_info[1].split(" ")
    # Достаем из строки последний элемент в котором содержится число питомцев
    all_pets_from_statistic = int(user_statistics_pets[-1])
    # Сверяем количество питмцев отображенных на странице равно статистике
    assert len(locator_for_all_my_pets) == all_pets_from_statistic


def test_half_of_my_pets_has_photo():
    """Тест на проверку, что как минимум половина питомцев имеет фото"""
    # Вводим email пользователя
    driver.find_element(By.ID, 'email').send_keys(valid_email)
    # Вводим пароль пользователя
    driver.find_element(By.ID, 'pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # Нажимаем кнопку "Мои питомцы" для вызова списка питомцев пользователя
    wait.until(EC.visibility_of_element_located((By.XPATH, '//a[contains(text(), "Мои питомцы")]'))).click()
    # Выбираем всех питомцев пользователя по локатору для кнопки удаления питомца
    locator_for_all_my_pets = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//td[@class="smart_cell"]')))

    # Выбираем все вебэлементы фотографий питомцев пользователя
    images = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//th/img')))

    # Назначаем новую переменную для подсчёта количества питомцев с фотографией
    number_of_pets_with_photo = 0

    # через проверку у всех питомцев, что attribute 'src' не пустое значение, определяем
    # количество питомцев с фотографией
    for i in range(len(locator_for_all_my_pets)):
        if images[i].get_attribute('src') != '':
            number_of_pets_with_photo += 1
        else:
            number_of_pets_with_photo = number_of_pets_with_photo

    # Проверяем, что как минимум половина всех питомцев имеет фотографию
    assert number_of_pets_with_photo >= (len(locator_for_all_my_pets) / 2)


def test_all_my_pets_has_name_type_age():
    """Тест для проверки, что у всех питомцев есть имя, порода и возраст"""
    # Вводим email пользователя
    driver.find_element(By.ID, 'email').send_keys(valid_email)
    # Вводим пароль пользователя
    driver.find_element(By.ID, 'pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # Нажимаем кнопку "Мои питомцы" для вызова списка питомцев пользователя
    wait.until(EC.visibility_of_element_located((By.XPATH, '//a[contains(text(), "Мои питомцы")]'))).click()
    # Выбираем всех питомцев пользователя по локатору для кнопки удаления питомца
    locator_for_all_my_pets = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//td[@class="smart_cell"]')))

    for i in range(len(locator_for_all_my_pets)):
        # для вебэлемента locator_for_all_my_pets (кнопка удаления питомца) находим все 3(три)
        # сосединие тэга "td" соответствующие имени, типу питомца и возрасту
        pet = locator_for_all_my_pets[i].find_elements(By.XPATH, 'preceding-sibling::td')
        # находим текст тэга "td" с индексом 2 соответсвующий имени питомца
        # и присваеваем переменной "name"
        name = wait.until(EC.visibility_of(pet[2])).text
        # находим текст тэга "td" с индексом 1 соответсвующий типу питомца
        # и присваеваем переменной "anymal_type"
        anymal_type = wait.until(EC.visibility_of(pet[1])).text
        # находим текст тэга "td" с индексом 0 соответсвующий возрасту питомца
        # и присваеваем переменной "age"
        age = wait.until(EC.visibility_of(pet[0])).text
        # проверяем, что у каждого питомца есть имя, тип питомца и возраст
        with soft_assertions():
            assert_that(name).is_not_equal_to('')
            assert_that(anymal_type).is_not_equal_to('')
            assert_that(age).is_not_equal_to('')


def test_all_my_pets_has_different_names():
    """Тест на прверку, что у всех питомцев разные имена"""
    # Вводим email пользователя
    driver.find_element(By.ID, 'email').send_keys(valid_email)
    # Вводим пароль пользователя
    driver.find_element(By.ID, 'pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # Нажимаем кнопку "Мои питомцы" для вызова списка питомцев пользователя
    wait.until(EC.visibility_of_element_located((By.XPATH, '//a[contains(text(), "Мои питомцы")]'))).click()
    # Выбираем всех питомцев пользователя по локатору для кнопки удаления питомца
    locator_for_all_my_pets = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//td[@class="smart_cell"]')))

    # Создаем пустой список для имён питомцев пользователя
    list_of_pets_names = []
    for i in range(len(locator_for_all_my_pets)):
        # для вебэлемента locator_for_all_my_pets (кнопка удаления питомца) находим все 3(три)
        # сосединие тэга "td" соответствующие имени, типу питомца и возрасту
        pet = locator_for_all_my_pets[i].find_elements(By.XPATH, 'preceding-sibling::td')
        # находим текст тэга "td" с индексом 2 соответсвующий имени питомца
        # и присваеваем переменной "name"
        name = wait.until(EC.visibility_of(pet[2])).text
        # добавляем имя питомца в список list_of_pets_names
        list_of_pets_names.append(name)
    # для проверки уникальности имени питомца, проверяем количество вхождений каждого
    # имени в списке имён питомцев
    with soft_assertions():
        for name in list_of_pets_names:
            assert_that(list_of_pets_names.count(name)).is_equal_to(1)


def test_all_my_pets_are_unique():
    """Тест что в списке нет повторяющихся питомцев"""
    # Вводим email пользователя
    driver.find_element(By.ID, 'email').send_keys(valid_email)
    # Вводим пароль пользователя
    driver.find_element(By.ID, 'pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # Нажимаем кнопку "Мои питомцы" для вызова списка питомцев пользователя
    wait.until(EC.visibility_of_element_located((By.XPATH, '//a[contains(text(), "Мои питомцы")]'))).click()
    # Создаем пустой список для полного описания питомцев пользователя
    list_of_pets_with_text_description = []
    # Выбираем всех питомцев пользователя по локатору для кнопки удаления питомца
    locator_for_all_my_pets = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//td[@class="smart_cell"]')))

    for i in range(len(locator_for_all_my_pets)):
        # для вебэлемента locator_for_all_my_pets (кнопка удаления питомца) находим все 3(три)
        # сосединие тэга "td" соответствующие имени, типу питомца и возрасту
        pet = locator_for_all_my_pets[i].find_elements(By.XPATH, 'preceding-sibling::td')
        # находим текст тэга "td" с индексом 2 соответсвующий имени питомца
        # и присваеваем переменной "name"
        name = wait.until(EC.visibility_of(pet[2])).text
        # находим текст тэга "td" с индексом 1 соответсвующий типу питомца
        # и присваеваем переменной "anymal_type"
        anymal_type = wait.until(EC.visibility_of(pet[1])).text
        # находим текст тэга "td" с индексом 0 соответсвующий возрасту питомца
        # и присваеваем переменной "age"
        age = wait.until(EC.visibility_of(pet[0])).text
        # создаем список для переменных name, anymal_type, age
        pet_list_type = [name, anymal_type, age]
        # объединяем строковые переменные name, anymal_type, age в одну pet_text
        pet_text = "".join(pet_list_type)
        # строковое описание питомца pet_text добавляем в список питомцев list_of_pets_with_text_description
        list_of_pets_with_text_description.append(pet_text)

    # для проверки уникальности каждого питомца, проверяем количество вхождений каждого
    # тескотового описания в списке всех питомцев
    with soft_assertions():
        for pet in list_of_pets_with_text_description:
            assert_that(list_of_pets_with_text_description.count(pet)).is_equal_to(1)

    driver.quit()
