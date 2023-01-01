import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest
import selenium
#driver = webdriver.Chrome()
@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('C:/1/chromedriver.exe')
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')
   pytest.driver.maximize_window()
   yield

   pytest.driver.quit()


def test_show_my_pets():
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


   images = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
   names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
   descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

   for i in range(len(names)):
      assert images[i].get_attribute('src') != ''
      assert names[i].text != ''
      assert descriptions[i].text != ''
      assert ', ' in descriptions[i]
      parts = descriptions[i].text.split(", ")
      assert len(parts[0]) > 0
      assert len(parts[1]) > 0


list_of_pets = pytest.driver.find_elements(By.XPATH, '/html/body/div[1]/div/div[1]/text()[1]')