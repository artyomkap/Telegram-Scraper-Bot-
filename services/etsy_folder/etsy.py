import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random
import requests
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


async def fetch_etsy_data():
    ua = UserAgent()
    user_agents_list = [ua.random for _ in range(30)]
    user_agent = random.choice(user_agents_list)

    options = Options()
    options.headless = True
    # Создаем веб-драйвер с заданными опциями
    driver = webdriver.Chrome(options=options)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    headers = {
        'User-Agent': user_agent
    }

    url = 'https://www.etsy.com/c/clothing?ref=catnav-374_dropdown'

    # Используем веб-драйвер для выполнения запроса
    driver.get(url)

    try:
        accept_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Принять')]"))
        )
        accept_button.click()
    except Exception as e:
        print(f"Не удалось найти кнопку 'Принять': {e}")

    # Пауза для загрузки данных (может потребоваться на различных сайтах)
    await asyncio.sleep(5)

    # Получаем содержимое страницы
    req = driver.page_source

    with open("etsy_html.html", "w", encoding="utf-8") as file:
        file.write(req)

    # Закрываем веб-драйвер
    driver.quit()

    with open("etsy_html.html", encoding="utf-8") as file:
        src = file.read()

    # Продолжаем обработку, как в вашем коде
    soup = BeautifulSoup(src, "lxml")
    items_div = soup.find("div", class_='wt-grid__item-xs-12 wt-pr-xs-1 wt-pl-xs-1 wt-pl-md-3 wt-pr-md-3')
    if items_div:
        items_div2 = items_div.find("div", class_="wt-bg-white wt-display-block wt-pb-xs-2 wt-mt-xs-0")
        print(items_div2)
        if items_div2:
            items_ol = items_div2.find("ol", class_="wt-grid wt-grid--block wt-pl-xs-0 tab-reorder-container")
            print(items_ol)


asyncio.run(fetch_etsy_data())
