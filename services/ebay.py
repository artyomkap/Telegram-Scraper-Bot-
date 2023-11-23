import asyncio
import json
import os
import time
import itertools
import random
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent






async def ebay_de_parser(search, sacat, min_price, max_price, sort_order, quantity):
    ua = UserAgent()
    user_agents_list = [ua.random for _ in range(30)]
    user_agent = random.choice(user_agents_list)
    headers = {
        "Accept-Ch": "sec-ch-ua-model,sec-ch-ua-platform-version,sec-ch-ua-full-version",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Cache-Control": "max-age=0",
        'User-Agent': user_agent
    }

    keyword = search
    min_price = min_price
    max_price = max_price
    sort_order = sort_order
    sacat = sacat




    url = f"https://www.ebay.de/sch/i.html?_from=R40&_nkw={keyword}&_sop={sort_order}&_udhi={max_price}&_udlo={min_price}&_ipg=120&_sacat={sacat}"

    print(url)


    req = requests.get(url, headers=headers).text

    with open("services/ebay_folder/ebay_de.html", "w", encoding="utf-8") as file:
        file.write(req)

    with open("services/ebay_folder/ebay_de.html", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    items = soup.find_all("li", class_="s-item s-item__pl-on-bottom")

    parsed_data = []


    items_number = int(quantity)

    for item in itertools.islice(items[1:], items_number):
        ua = UserAgent()
        user_agents_list = [ua.random for _ in range(30)]
        user_agent = random.choice(user_agents_list)
        headers_item = {
            "Accept-Ch": "sec-ch-ua-model,sec-ch-ua-platform-version,sec-ch-ua-full-version",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Cache-Control": "max-age=0",
            'User-Agent': user_agent
        }


        item_name_href = item.find(class_="s-item__title")
        item_name = item_name_href.text.replace("Neues Angebot", "", 1).replace("*New*", "").strip()
        item_price_href = item.find(class_="s-item__price")
        item_price = item_price_href.text
        item_link = item.find(class_="s-item__link").get("href")
        item_picture_url = item.find(class_="s-item__image-wrapper image-treatment").find("img").get("src")

        src_item = requests.get(item_link, headers=headers_item).text
        soup_item = BeautifulSoup(src_item, "lxml")
        item_condition = None
        item_condition_href = soup_item.find("div", class_="x-item-condition-value")
        if item_condition_href:
            item_condition = item_condition_href.find("span", class_="ux-textspans").text
        seller_name = soup_item.find("div", class_="d-stores-info-categories__container__info__section").find("h2", class_="d-stores-info-categories__container__info__section__title").find("span", class_="ux-textspans ux-textspans--BOLD").text
        seller_link = soup_item.find(class_="ux-seller-section__item--seller").find("a").get("href")
        feedback_text = soup_item.find("div", class_="d-stores-info-categories__container__info__section")
        if feedback_text is None:
            feedback_text = "Не найдено"
        else:
            feedback_text_get = soup_item.find("div", class_="d-stores-info-categories__container__info__section").find("div", class_="d-stores-info-categories__container__info__section__item")
            if feedback_text_get is None:
                feedback_text = "Не найдено"
            else:
                feedback_text = soup_item.find("div", class_="d-stores-info-categories__container__info__section").find("div", class_="d-stores-info-categories__container__info__section__item").find("span", class_="ux-textspans ux-textspans--BOLD").text

        div_elements = soup_item.find_all("div", class_="d-stores-info-categories__container__info__section__item")
        if len(div_elements) >= 2:
            second_div = div_elements[1]

            items_sold = second_div.find("span", class_="ux-textspans ux-textspans--BOLD").text


            item_data = {
                "Name": item_name,
                "Price": item_price,
                "Item Picture": item_picture_url,
                "Item Link": item_link,
                "Item Condition": item_condition if item_condition is not None else "N/A",
                "Seller Nickname": seller_name,
                "Seller Link": seller_link,
                "Seller Feedback": feedback_text,
                "Seller Sold Items": items_sold

            }

        # Добавьте словарь с данными в список
            parsed_data.append(item_data)

            # Сохраните список словарей в JSON файл
            json_file_path = "services/ebay_folder/ebay_de_output.json"
            with open(json_file_path, "w", encoding="utf-8") as json_file:
                json.dump(parsed_data, json_file, ensure_ascii=False, indent=4)


    file_path = "services/ebay_folder/ebay_de.html"
    if os.path.exists(file_path):
        # Если файл существует, удаляем его
        os.remove(file_path)
        print(f"Файл {file_path} успешно удален.")
    else:
        # Если файл не существует, выводим сообщение об этом
        print(f"Файл {file_path} не существует.")

    return "Finished"

