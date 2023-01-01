import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Chrome()


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('C:/1/chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    pytest.driver.maximize_window()
    yield

    pytest.driver.quit()

#---------------------------------------------------------------------------------
# Проверка входа в личный кабинет пользователя
def test_show_my_pets():
    pytest.driver.implicitly_wait(20)
    # Вводим email
    pytest.driver.find_element(By.ID,'email').send_keys('studentpm@mail.ru')
    # Вводим пароль
    pytest.driver.find_element(By.ID,'pass').send_keys('2236')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR,'button[type="submit"]').click()
    pytest.driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()

    time.sleep(5)
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.ID,'all_my_pets')


#---------------------------------------------------------------------------------
# Проверка отображения в личном кабинете всех питомцев пользователя
def test_all_pets_displayed_in_personal_account():
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('studentpm@mail.ru')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('2236')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Нажимаем на кнопку входа в личный кабинет со списком питомцев
    pytest.driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()
    # Получаем список имен всех питомцев и сохраняем в переменную names
    names = pytest.driver.find_elements(By.XPATH, '(//*[@id="all_my_pets"]/table/tbody/tr/td[1])')
    pets_names = []
    for x in names:
       names = x.text
       pets_names.append(names)
    print("\nКоличество питомцев отображающихся  в личном кабинете =", len( pets_names))
    print(pets_names)
    # Получем количество питомцев пользователя
    number_of_pets = pytest.driver.find_element(By.XPATH, '(html/body/div[1]/div[1]/div[1])').text
    num = list(map(int, re.compile(r'(?<=Питомцев: )\d+').findall(number_of_pets)))
    num_1 = int(''.join(map(str, num)))
    print("Количество питомцев которые должны отображаться в личном кабинете =", num_1)
    # Проверяем что все питомцы отображаются в личном кабинете
    assert len(pets_names) == num_1

# ---------------------------------------------------------------------------------
# Проверка что хотя бы у половины питомцев есть фотография
def test_check_photo_of_pets():
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('studentpm@mail.ru')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('2236')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Нажимаем на кнопку входа в личный кабинет со списком питомцев
    pytest.driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()

    photo = pytest.driver.find_elements(By.CSS_SELECTOR, 'th>img')
    uploaded_photo = 0

    for i in range(len(photo)):
        if photo[i].get_attribute('src') != "":
          uploaded_photo += 1
        else:
          uploaded_photo += 0

    # Получем количество питомцев пользователя
    number_of_pets = pytest.driver.find_element(By.XPATH, '(html/body/div[1]/div[1]/div[1])').text
    num = list(map(int, re.compile(r'(?<=Питомцев: )\d+').findall(number_of_pets)))
    num_1 = int(''.join(map(str, num)))
    print("\nКоличество питомцев пользователя =", num_1)
    print("\nКоличество загруженных фото питомцев =", uploaded_photo)
    assert uploaded_photo >= num_1/2

# ---------------------------------------------------------------------------------
# Проверка что у всех питомцев разные имена
def test_all_pets_have_different_names():
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('studentpm@mail.ru')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('2236')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Нажимаем на кнопку входа в личный кабинет со списком питомцев
    pytest.driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()
    # Получаем список имен всех питомцев и сохраняем в переменную names
    names = pytest.driver.find_elements(By.XPATH, '(//*[@id="all_my_pets"]/table/tbody/tr/td[1])')
    pets_names = []
    for x in names:
        names = x.text
        pets_names.append(names)
    unique_names = set(pets_names)
    print("\nУникальные имена питомцев: ", unique_names)
    print("\nИмена всех питомцев: ", pets_names)
    assert len(pets_names) == len(unique_names)

# ---------------------------------------------------------------------------------
# Проверка что у всех питомцев есть имя, возраст и порода.
def test_all_pets_have_name_breed_age():
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('studentpm@mail.ru')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('2236')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Нажимаем на кнопку входа в личный кабинет со списком питомцев
    pytest.driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()
    # Получаем список имен всех питомцев и сохраняем в переменную names
    names = pytest.driver.find_elements(By.XPATH, '(//*[@id="all_my_pets"]/table/tbody/tr/td[1])')
    # Получаем список пород всех питомцев и сохраняем в переменную breed
    breeds = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
    # Получаем возраст всех питомцев и сохраняем в переменную ages
    ages = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')
    # Проверяем что имя, порода и возраст не пустые значения
    for i in range(len(names)):
        assert names[i] != ''

    for i in range(len(breeds)):
        assert breeds[i] != ''

    for i in range(len(ages)):
        assert ages[i] != ''

# ---------------------------------------------------------------------------------
# Проверка что в списке нет повторяющихся питомцев
def test_all_pets_are_unique():
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('studentpm@mail.ru')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('2236')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Нажимаем на кнопку входа в личный кабинет со списком питомцев
    pytest.driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()
    # Получаем список  всех питомцев и сохраняем в переменную pets
    pets = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '(//*[@id="all_my_pets"]/table/tbody/tr)')))
    # pets = pytest.driver.find_elements(By.XPATH, '(//*[@id="all_my_pets"]/table/tbody/tr)')
    list_pets = []

    for x in pets:
        pets = x.text.replace(' ', '')
        pets = pets.replace('×', '')
        pets = pets.replace('\n', '')
        list_pets.append(pets)


    set_pets = set(list_pets)
    assert len(set_pets) == len(list_pets)
    print('\nКоличество уникальных питомцев пользователя: ', len(set_pets))
    print('\nКоличество всех питомцев пользователя: ', len(list_pets))












