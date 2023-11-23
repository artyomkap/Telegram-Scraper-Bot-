import asyncio
import json
import os
import time
import itertools
import random
from app import database as db
import aiofiles
import fasteners
import requests
from aiogram.client.session import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import datetime


async def fetch(url, session, headers):
    async with session.get(url) as response:
        return await response.text()


async def klein_links_parsing(user_id, links):

    async def generate_links2(link, number_of_parsing):
        new_urls = []  # Переместили инициализацию внутрь функции
        for i in range((number_of_parsing - 1) * 3 + 3, number_of_parsing * 3 + 3):
            new_link = f"{link}/seite:{i}/"
            new_urls.append(new_link)

        return new_urls

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
    all_items = []
    new_links = None
    print(links)
    for link in links:
        new_urls = []  # Инициализация для каждой ссылки
        url_parsings = await db.get_klein_parsings(user_id, link)
        if url_parsings == "not found" or url_parsings is None:
            await db.add_klein_parsings(user_id, link)
            for i in range(1, 4):
                new_url = f"{link}/seite:{i}/"
                new_urls.append(new_url)
        else:
            for url_parsing in url_parsings:
                number_of_parsings = url_parsing[2]
                time_of_parsing = url_parsing[3]
                current_time = int(time.time())
                time_difference = current_time - time_of_parsing
                if time_difference >= 12 * 3600:
                    await db.delete_klein_parsings(user_id, link)
                    for i in range(1, 4):
                        new_url = f"{link}/seite:{i}/"
                        new_urls.append(new_url)
                else:
                    new_links = await generate_links2(link, number_of_parsings)
                    await db.update_klein_parsings(user_id, link)

        if new_urls:
            for url in new_urls:
                print("Ссылка в случае новой ссылке:", url)
                req = requests.get(url, headers=headers).text
                soup = BeautifulSoup(req, "lxml")
                items1 = soup.find_all("li", class_="ad-listitem")
                items2 = soup.find_all("li", class_="ad-listitem    badge-topad is-topad  ")
                items3 = soup.find_all("li", class_="ad-listitem    ")
                page_items = items1 + items2 + items3
                all_items.extend(page_items)

        if new_links:
            for url in new_links:
                print("Ссылка в случае повторения:", url)
                req = requests.get(url, headers=headers).text
                soup = BeautifulSoup(req, "lxml")
                items1 = soup.find_all("li", class_="ad-listitem")
                items2 = soup.find_all("li", class_="ad-listitem    badge-topad is-topad  ")
                items3 = soup.find_all("li", class_="ad-listitem    ")
                page_items = items1 + items2 + items3
                all_items.extend(page_items)

    total_items = len(all_items)
    print(f"Общее количество найденных товаров: {total_items}")
    if all_items:
        items = all_items
        await scrape_data_in_items_links(items)





async def klein_parser_url(user_id, user_url, quantity):
    url = user_url
    parse = await klein_parser(user_id, url, quantity)
    if parse == "Finished":
        return "Finished"


async def klein_parsing_with_filters(user_id, category, search, priceMax, priceMin, sort, quantity):
    if sort == "":
        url = f"https://www.kleinanzeigen.de/preis:{priceMin}:{priceMax}/{search}/k0{category}"
        print(url)
    else:
        url = f"https://www.kleinanzeigen.de/{sort}/preis:{priceMin}:{priceMax}/{search}/k0{category}"
        print(url)
    parse = await klein_parser(user_id, url, quantity)
    if parse == "Finished":
        return "Finished", url




async def klein_parser(user_id, url, quantity):
    async def generate_links(base_url, number_of_parsing):
        links = []

        # В цикле формируем ссылки для каждой страницы
        for i in range(number_of_parsing * 10 + 1, number_of_parsing * 10 + 11):
            link = f"{base_url}/seite:{i}/"
            links.append(link)

        return links


    async def parser_link(user_id, url, quantity):
        await db.add_klein_parsings(user_id, url)
        req = None
        try:
            req = requests.get(url, headers=headers)
            req.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error accessing the URL: {e}")
        req = req.text
        with open("services/kleinanzeigen/klein_parse.html", "w", encoding="utf-8") as file:
            file.write(req)

        with open("services/kleinanzeigen/klein_parse.html", encoding="utf-8") as file:
            src1 = file.read()

        soup1 = BeautifulSoup(src1, "lxml")
        count_pages = soup1.find("div", class_="pagination-pages")
        if count_pages:
            pages = count_pages.find_all("a", class_="pagination-page")
            if pages:
                for page in pages:
                    page_url = domen + page.get("href")
                    r = requests.get(page_url, headers=headers).text
                    soup = BeautifulSoup(r, "lxml")
                    items1 = soup.find_all("li", class_="ad-listitem")
                    items2 = soup.find_all("li", class_="ad-listitem    badge-topad is-topad  ")
                    items3 = soup.find_all("li", class_="ad-listitem    ")
                    page_items = items1 + items2 + items3
                    all_items.extend(page_items)
                    await asyncio.sleep(0.2)

        with open("services/kleinanzeigen/klein_parse.html", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        items1 = soup.find_all("li", class_="ad-listitem")
        items2 = soup.find_all("li", class_="ad-listitem    badge-topad is-topad  ")
        items3 = soup.find_all("li", class_="ad-listitem    ")

        new_items = items1 + items2 + items3

        items = new_items + all_items

        total_items = len(items)
        print(f"Общее количество найденных товаров: {total_items}")

        await scrape_data_in_items(items)



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
    print("Ссылка для парсинга", url)
    domen = "https://www.kleinanzeigen.de"
    all_items = []
    parsed_data = []
    items1 = None
    items2 = None
    items3 = None
    url_parsings = await db.get_klein_parsings(user_id, url)
    print("url_parsings = ", url_parsings)
    if url_parsings == "not found" or url_parsings is None:
        await parser_link(user_id, url, quantity)
    else:
        for url_parsing in url_parsings:
            number_of_parsings = url_parsing[2]
            time_of_parsing = url_parsing[3]
            current_time = int(time.time())
            time_difference = current_time - time_of_parsing
            if time_difference >= 12 * 3600:
                await db.delete_klein_parsings(user_id, url)
                all_items = await parser_link(user_id, url, quantity)
            else:
                result_links = await generate_links(url, number_of_parsings)
                for link in result_links:
                    r = requests.get(link, headers=headers).text
                    soup = BeautifulSoup(r, "lxml")
                    items1 = soup.find_all("li", class_="ad-listitem")
                    items2 = soup.find_all("li", class_="ad-listitem    badge-topad is-topad  ")
                    items3 = soup.find_all("li", class_="ad-listitem    ")
                    page_items = items1 + items2 + items3
                    all_items.extend(page_items)
                    await asyncio.sleep(0.2)
                await db.update_klein_parsings(user_id, url)

        items = all_items
        total_items = len(items)
        print(f"Общее количество найденных товаров: {total_items}")
        await scrape_data_in_items_links(items)


async def scrape_data_in_items(items):
    print("Начал сбор данных с товаров")

    domen = "https://www.kleinanzeigen.de"
    parsed_data = []

    for item in items:
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

        item_seller = None
        seller_link = None
        item_href = None
        item_name = None
        item_picture = None
        item_price = None


        item_href1 = item.find('h2', class_="text-module-begin")
        item_href2 = item.find('a', class_="p_ si65 a")



        if item_href1:
            item_href = domen + item_href1.find('a', class_="ellipsis").get("href")
            item_name = item_href1.find('a', class_="ellipsis").text
        elif item_href2:
            item_href = domen + item_href2.get("href")
            item_name = item_href2.text
        else:
            pass


        item_picture_href1 = item.find("div", class_="imagebox srpimagebox")
        item_picture_href2 = item.find("div", class_="i_ div si33")


        if item_picture_href1:
            item_picture = item_picture_href1.find('img').get("src")
        elif item_picture_href2:
            item_picture = item_picture_href2.find("img").get("src")

        item_date = None
        item_date1 = item.find("div", class_="aditem-main--top--right")
        if item_date1:
            item_date = item_date1.text.strip()


        item_shipping = None
        item_shipping_href = item.find("div", class_="aditem-main--middle--price-shipping")
        if item_shipping_href:
            item_shipping_p = item_shipping_href.find("p", class_="aditem-main--middle--price-shipping--shipping")
            if item_shipping_p:
                item_shipping = item_shipping_p.text.strip()
                if item_shipping:
                    item_shipping = "Возможна доставка"



        item_price1 = item.find("div", class_="aditem-main--middle--price-shipping")
        item_price2 = item.find("p", class_="aditem-main--middle--price-shipping--price")
        item_price3 = item.find("div", class_="i_ div si136")
        if item_price1:
            item_price = item_price1.find("p", class_="aditem-main--middle--price-shipping--price").text.strip()
        elif item_price2:
            item_price = item_price2.text.strip()
        elif item_price3:
            item_price = item_price3.find("span", class_="p_  span").text


        item_description1 = item.find("p", class_="aditem-main--middle--description")
        if item_description1:
            item_description = item_description1.text.strip()
        else:
            item_description = "Отсутсвует"


        if item_href:
            soup_item = None
            src_item = requests.get(item_href, headers=headers_item).text
            soup_item = BeautifulSoup(src_item, "lxml")
        else:
            continue



        seller_date = None
        seller_date_container = soup_item.find("div", class_="l-container-row contentbox--vip no-shadow j-sidebar-content")
        if seller_date_container:
            seller_date_li = seller_date_container.find("span", class_="text-body-regular text-light")
            if seller_date_li:
                seller_date = seller_date_li.text.strip()
                lines = seller_date.splitlines()
                seller_date = lines[1].strip()


        item_seller1 = soup_item.find("span", class_="text-body-regular-strong text-force-linebreak")
        if item_seller1:
            seller_href = item_seller1.find("a")
            if seller_href:
                seller_link = domen + seller_href.get("href")
                item_seller = seller_href.text.strip()
            else:
                item_seller = item_seller1.text.strip()


        seller_feedback = None
        seller_feedback1 = soup_item.find("span", class_="userbadges-vip userbadges-profile-rating")
        if seller_feedback1:
            seller_feedback = seller_feedback1.find("span", class_="text-light").text.strip()


        seller_items = None
        if seller_link:
            seller_item = requests.get(seller_link, headers=headers_item).text
            soup_seller = BeautifulSoup(seller_item, "lxml")
        else:
            continue



        seller_items1 = soup_seller.find_all("span", class_="userprofile-details")
        if len(seller_items1) >= 3:
            seller_items = seller_items1[2].text.strip()
            seller_items = ' '.join(seller_items.split())
            seller_items = seller_items.replace("\n", " ")
            seller_items = seller_items.replace("Anzeigen online", "Товары в продаже")
            seller_items = seller_items.replace("gesamt", "всего")



        item_data = {
            "Name": item_name if item_name is not None else "Имя товара не указано",
            "Price": item_price if item_price is not None else "Цена не указана",
            "Item Picture": item_picture if item_picture is not None else "Картинка отсутствует",
            "Item Link": item_href,
            "Item Description": item_description.replace("\n", ""),
            "Item Publish Date": item_date if item_date is not None else "Дата публикации отсутствует",
            "Item Shipping": item_shipping if item_shipping is not None else "Доставки нет",
            "Seller Nickname": item_seller.replace("\n", " "),
            "Seller Link": seller_link,
            "Seller Registration Date": seller_date,
            "Seller Feedback": seller_feedback if seller_feedback is not None else "Отзывы отсутствуют",
            "Seller Items": seller_items

        }

        if item_data:
            parsed_data.append(item_data)

        json_file_path = "services/kleinanzeigen/klein_output.json"
        async with aiofiles.open(json_file_path, "w+", encoding="utf-8") as json_file:
            await json_file.write(json.dumps(parsed_data, ensure_ascii=False, indent=4))



    print("парсинг завершен")
    return "Finished"




async def scrape_data_in_items_links(items):
    print("Начал сбор данных с товаров")

    domen = "https://www.kleinanzeigen.de"
    parsed_data = []

    for item in items:
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

        item_seller = None
        seller_link = None
        item_href = None
        item_name = None
        item_picture = None
        item_price = None


        item_href1 = item.find('h2', class_="text-module-begin")
        item_href2 = item.find('a', class_="p_ si65 a")



        if item_href1:
            item_href = domen + item_href1.find('a', class_="ellipsis").get("href")
            item_name = item_href1.find('a', class_="ellipsis").text
        elif item_href2:
            item_href = domen + item_href2.get("href")
            item_name = item_href2.text
        else:
            pass


        item_picture_href1 = item.find("div", class_="imagebox srpimagebox")
        item_picture_href2 = item.find("div", class_="i_ div si33")


        if item_picture_href1:
            item_picture = item_picture_href1.find('img').get("src")
        elif item_picture_href2:
            item_picture = item_picture_href2.find("img").get("src")

        item_date = None
        item_date1 = item.find("div", class_="aditem-main--top--right")
        if item_date1:
            item_date = item_date1.text.strip()


        item_shipping = None
        item_shipping_href = item.find("div", class_="aditem-main--middle--price-shipping")
        if item_shipping_href:
            item_shipping_p = item_shipping_href.find("p", class_="aditem-main--middle--price-shipping--shipping")
            if item_shipping_p:
                item_shipping = item_shipping_p.text.strip()
                if item_shipping:
                    item_shipping = "Возможна доставка"



        item_price1 = item.find("div", class_="aditem-main--middle--price-shipping")
        item_price2 = item.find("p", class_="aditem-main--middle--price-shipping--price")
        item_price3 = item.find("div", class_="i_ div si136")
        if item_price1:
            item_price = item_price1.find("p", class_="aditem-main--middle--price-shipping--price").text.strip()
        elif item_price2:
            item_price = item_price2.text.strip()
        elif item_price3:
            item_price = item_price3.find("span", class_="p_  span").text


        item_description1 = item.find("p", class_="aditem-main--middle--description")
        if item_description1:
            item_description = item_description1.text.strip()
        else:
            item_description = "Отсутсвует"


        if item_href:
            soup_item = None
            src_item = requests.get(item_href, headers=headers_item).text
            soup_item = BeautifulSoup(src_item, "lxml")
        else:
            continue



        seller_date = None
        seller_date_container = soup_item.find("div", class_="l-container-row contentbox--vip no-shadow j-sidebar-content")
        if seller_date_container:
            seller_date_li = seller_date_container.find("span", class_="text-body-regular text-light")
            if seller_date_li:
                seller_date = seller_date_li.text.strip()
                lines = seller_date.splitlines()
                seller_date = lines[1].strip()


        item_seller1 = soup_item.find("span", class_="text-body-regular-strong text-force-linebreak")
        if item_seller1:
            seller_href = item_seller1.find("a")
            if seller_href:
                seller_link = domen + seller_href.get("href")
                item_seller = seller_href.text.strip()
            else:
                item_seller = item_seller1.text.strip()


        seller_feedback = None
        seller_feedback1 = soup_item.find("span", class_="userbadges-vip userbadges-profile-rating")
        if seller_feedback1:
            seller_feedback = seller_feedback1.find("span", class_="text-light").text.strip()


        seller_items = None
        if seller_link:
            seller_item = requests.get(seller_link, headers=headers_item).text
            soup_seller = BeautifulSoup(seller_item, "lxml")
        else:
            continue



        seller_items1 = soup_seller.find_all("span", class_="userprofile-details")
        if len(seller_items1) >= 3:
            seller_items = seller_items1[2].text.strip()
            seller_items = ' '.join(seller_items.split())
            seller_items = seller_items.replace("\n", " ")
            seller_items = seller_items.replace("Anzeigen online", "Товары в продаже")
            seller_items = seller_items.replace("gesamt", "всего")



        item_data = {
            "Name": item_name if item_name is not None else "Имя товара не указано",
            "Price": item_price if item_price is not None else "Цена не указана",
            "Item Picture": item_picture if item_picture is not None else "Картинка отсутствует",
            "Item Link": item_href,
            "Item Description": item_description.replace("\n", ""),
            "Item Publish Date": item_date if item_date is not None else "Дата публикации отсутствует",
            "Item Shipping": item_shipping if item_shipping is not None else "Доставки нет",
            "Seller Nickname": item_seller.replace("\n", " "),
            "Seller Link": seller_link,
            "Seller Registration Date": seller_date,
            "Seller Feedback": seller_feedback if seller_feedback is not None else "Отзывы отсутствуют",
            "Seller Items": seller_items

        }

        if item_data:
            parsed_data.append(item_data)

        json_file_path = "services/kleinanzeigen/klein_output.json"
        async with aiofiles.open(json_file_path, "w+", encoding="utf-8") as json_file:
            await json_file.write(json.dumps(parsed_data, ensure_ascii=False, indent=4))



    print("парсинг завершен")
    return "Finished"

