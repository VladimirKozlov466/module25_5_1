from selenium import webdriver
from selenium.webdriver.chrome.service import Service


# Указываем путь до chromedriver и присваеваем его объекту driver webdriver используемого браузера
s = Service('/Users/driverChrome/chromedriver')
driver = webdriver.Chrome(service=s)