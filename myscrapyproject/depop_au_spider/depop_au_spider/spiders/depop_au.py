import json
import requests
import scrapy
from bs4 import BeautifulSoup
import fake_useragent
import logging


logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('scrapy').setLevel(logging.ERROR)


class DepopAuSpider(scrapy.Spider):
    name = "depop_au"
    allowed_domains = ["depop.com", "webapi.depop.com"]

    def __init__(self, search=None, priceMax=None, priceMin=None, sort=None, quantity=None, country=None, *args, **kwargs):
        super(DepopAuSpider, self).__init__(*args, **kwargs)
        self.search = search
        self.priceMax = priceMax
        self.priceMin = priceMin
        self.sort = sort
        self.quantity = quantity
        self.country = country
        if country == "au":
            currency = "AUD"
        elif country == "de":
            currency = "EUR"
        elif country == "fr":
            currency = "EUR"
        elif country == "gb":
            currency = "GBP"
        elif country == "it":
            currency = "EUR"
        elif country == "us":
            currency = "USD"
        if priceMax and priceMin is None:
            self.start_urls = [f"https://webapi.depop.com/api/v2/search/products/?what={search}&itemsPerPage=70&country={country}&currency={currency}&sort={sort}"]
        else:
            self.start_urls = [f"https://webapi.depop.com/api/v2/search/products/?what={search}&itemsPerPage={quantity}&country={country}&currency={currency}&sort={sort}&priceMax={priceMax}&priceMin={priceMin}"]


    def parse(self, response, **kwargs):
        user_agent = fake_useragent.UserAgent().random
        headers = dict(user_agent=user_agent)
        data = json.loads(response.body)
        products = data.get('products', [])
        scraped_data = []

        for index, product in enumerate(products, start=1):
            product_id = product.get('id')
            slug = product.get('slug')
            item_link = f"https://www.depop.com/products/{slug}/"
            requests_item = requests.get(item_link, headers=headers)
            src_item = requests_item.text
            soup_item = BeautifulSoup(src_item, "lxml")
            item_description_text = soup_item.find(class_="sc-eDnWTT styles__TextContainer-sc-79aebd3a-1 kcKICQ lktLQq")
            price_tax = product.get('price', {}).get('taxInclusivepriceAmount')
            if price_tax is None or price_tax == "0" or price_tax == "None":
                price_tax = product.get('price', {}).get('priceAmount')
            product_data = {
                "Product_Number": index,
                "ID": product_id,
                "Slug": slug,
                "Date Created": product.get('dateCreated'),
                "Price": price_tax,
                "Currency": product.get('price', {}).get('currencyName'),
                "Item Link": item_link,
                "Item Description": item_description_text.text.strip().replace("\n", " ") if item_description_text else "N/A",
                "Item Picture": product.get('preview', {}).get('1280')
            }



            seller_name_text = soup_item.find(class_="sc-eDnWTT styles__Username-sc-46110958-3 fRxqiS kKpWIW")
            if seller_name_text is None:
                seller_name = "N/A"
                product_data["Seller Nickname"] = seller_name
            else:
                seller_name = seller_name_text.text.strip()
                product_data["Seller Nickname"] = seller_name

                seller_link = f"https://www.depop.com/{seller_name}/"
                if seller_link == "N/A":
                    seller_followers = "N/A"
                    product_data["Seller Link"] = "N/A"
                else:
                    product_data["Seller Link"] = seller_link

                    request_seller = requests.get(seller_link, headers=headers)
                    src_seller = request_seller.text
                    soup_seller = BeautifulSoup(src_seller, "lxml")
                    seller_followers_text = soup_seller.find(class_="sc-eDnWTT styles__StatsValue-sc-c1872ee6-0 fRxqiS lhsWNI")

                    if seller_followers_text is None:
                        seller_followers = "N/A"
                        product_data["Seller Followers"] = seller_followers
                    else:
                        seller_followers = seller_followers_text.text.strip()
                        product_data["Seller Followers"] = seller_followers



            # Вывод данных или выполнение других действий

            scraped_data.append(product_data)
            # Write the scraped data to a JSON file


        with open("scraped_data_depop.json", 'w', encoding='utf-8') as json_file:
            json.dump(scraped_data, json_file, ensure_ascii=False, indent=4)

            # print(f"\nProduct_Number: {index}, ID: {product_id}, Slug: {slug}, Date Created: {date_created}, Price: {price_amount} {price_currency}, Item Description: {item_description}")
            # print(f"Seller Nickname: {seller_name}, Seller Followers: {seller_followers} Followers")
            # print(f"Preview 1280: {preview_1280}")
