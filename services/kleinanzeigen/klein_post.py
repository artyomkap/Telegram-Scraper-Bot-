import random
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json

ua = UserAgent()
user_agents_list = [ua.random for _ in range(30)]
user_agent = random.choice(user_agents_list)
headers = {
    "Accept-Ch": "sec-ch-ua-model,sec-ch-ua-platform-version,sec-ch-ua-full-version",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Cache-Control": "max-age=0",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

# Преобразование строки JSON в словарь
cookies_str = '[{"name":"access_token","value":"eyJhbGciOiJSUzI1NiIsImtpZCI6IjgyYjFjNmYwLWRiM2EtNTQ2Ny1hYmI2LTJlMzAxNDViZjc3MiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50X2lkIjoiYmI4OGJhMGQtMGYxNi00NzA0LTlmMWUtYWY3Yjc4MTFlNWQ3IiwiY2xpZW50X2lkIjoia2EtbGVnYWN5LXdlYiIsImRlcHJlY2F0ZWRfc3RvcmVfaWQiOjAsImV4cCI6MTcwMDIxMjc5NywiaWF0IjoxNzAwMjA1NTk3LCJpbnN0YWxsX2lkIjoiMmE0ODcxYzktZjJkOS00MDIwLThjZTAtMDg5MWIwMmJkMzY3IiwiaXNzIjoiaHR0cHM6Ly9hdXRoLmxlYm9uY29pbi5mciIsImp0aSI6IjcxNDc1ODQ5LWRkNTQtNDdlZC1iNzMxLThhYmQ2ZjlmMzBiZiIsInByZWZlcnJlZF91c2VybmFtZSI6IjEzNTY0MjgxOSIsInJlZnVzZWRfc2NvcGUiOiIiLCJyZWZ1c2VkX3Njb3BlcyI6bnVsbCwic2NvcGUiOiJvZmZsaW5lIG9wZW5pZCBwcm9maWxlIHVybjplYmF5LWtsZWluYW56ZWlnZW46dXNlciIsInNjb3BlcyI6WyJvZmZsaW5lIl0sInNlc3Npb25faWQiOiI5YjA4OTc4MC1mOTc3LTRiOGMtYmFhNy0zZjJiNTgxYjk2NjQiLCJzaWQiOiI5YjA4OTc4MC1mOTc3LTRiOGMtYmFhNy0zZjJiNTgxYjk2NjQiLCJzdWIiOiJiYjg4YmEwZC0wZjE2LTQ3MDQtOWYxZS1hZjdiNzgxMWU1ZDcifQ.Lkykf-ny5_rdhIaXSUpQsFdB7F-IVaHGEi00kNcLvS2wzLuyoCQm9xQZgUUPRRVGfTwuzsF37m3pcUlS2pK1FjS6JX4Yj3yMRYW3TsdjG89sPF1ikZ3j_JKpMIZOl0Gs_mN70-P6HTtvWkHrz4F2Nokg05jXggH0OWOabIGTiOyC6Nj9FhE-Nx02w8Dn35H1a4tvyFhEpYHTyIcbg_ghAe-vSLpV8hT1rxPqS6hrJU0Wk3MGTNOskRk0YlyOsJXz-QynfyiIrATqbPYBq9NzOc9klJElR0denwZe5IGYZtSVCFW1sn74MmFfktr-EzipzpKQT9FmQPSL9und858_-Ad9MxNnymsn8aVf_IZtzUtwpDXKHKEPr8No8RebIBWFYzWvJPuuaabvfQ0RdG1puu5-yAxlco6Ve5H8yB-3hLeBtbvz5ElekokiEIUinUCGuL2Xc_iK8S-wig36pCIGfTsc-AwGczXnXNgXBblBsFe00ieOM0HCZ40TsNsVZlNfJOJWrT89Yd9WyxLMPBMCQ7cCXe0NOjvVHr2wYtJAyv0JxnUCoJfD7HZRaO6exvGuIoRL0E6WONjC6uNen5LUd6J_yzv6YyDNRzueo-DprRcjuUhDA3WyyVkcRcR1TLjh8eeL4lD1uv-2V755DaL7OjHAXRoyU8mw1w9PvBj_dbw","domain":"www.kleinanzeigen.de","path":"/","expirationDate":1700291997.745988},{"name":"refresh_token","value":"eyJhbGciOiJSUzI1NiIsImtpZCI6IjgyYjFjNmYwLWRiM2EtNTQ2Ny1hYmI2LTJlMzAxNDViZjc3MiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaWQiOiJrYS1sZWdhY3ktd2ViIiwiaWF0IjoxNzAwMjA1NTk3LCJpbnN0YWxsX2lkIjoiMmE0ODcxYzktZjJkOS00MDIwLThjZTAtMDg5MWIwMmJkMzY3IiwianRpIjoiZDU3MjJiMjctNGEyZC00YWU4LTlhYTEtMmViYjhlYzRiYzFjIiwicmVxdWVzdGVkX3Njb3BlIjpbIm9mZmxpbmUiXSwic2Vzc2lvbl9pZCI6IjliMDg5NzgwLWY5NzctNGI4Yy1iYWE3LTNmMmI1ODFiOTY2NCIsInN1YiI6ImxiYztiYjg4YmEwZC0wZjE2LTQ3MDQtOWYxZS1hZjdiNzgxMWU1ZDc7MCJ9.f1wUqUv7OkQafdPf_D0cSJYzHH1KW8IIC_0hg75IAue2lR6cLHQSQzMrizltCUkP7Sfx5-VhiAZ9JGqsAWXGlzDbotsXITiC774rIw_1kA2nw-bA6JcqMY56iGThThfru5MS-rCe4dB2dV-pA24HapUWsIRKprg-GW9oCq2b9cgEp5GoL41VrOIQXnsYj8V0EVNdEI0Pfu8r7EO1tS9o6cb7qdKprMywLOl9gx6LZRpLII-0RsX_TxIc9QhipqmmoNLe6Eh59pGSaVi2IVAV_tnFvHL5ab-H7I9dQKNBWQGxnxGG7-Z6HIaafRaaYSMicPtQnWwysAKdeWvU8-Yr-3soVTnMOuiLtcFO6nrwaRhOAWlRt6WSZaNkORusfCdvoLgqmzXDVUu9_Gq7GWtfFusa7RmxGu7JS8lLWAMULmy0xiORXn__UkZEwfK5OJf88z6ztIbNwYbFLQJwuHN9dKsNWHasBF7GDahAeSEB0Jmw3eYo77xht9ZPn8jjwHJzTX0JQy9H2jFs3Hfi8H6FW8jXj338NeQL0TxiyBJP4s1IHwx7VgePSsPi_f8YFUNsUPnZ-9CLX3VrKWDuPMGIXD4vUy4Jfj1Lw6rmRx6DG0CqkKt2miBZVhVhnoyI-7OT25wPZbXpQcsivvgNANN3TPdwhpJ2gm68TkC9HKo52EU","domain":"www.kleinanzeigen.de","path":"/","expirationDate":1715757597.746093}]'
cookies_list = json.loads(cookies_str)

# Преобразование в словарь кук
cookies = {cookie["name"]: cookie["value"] for cookie in cookies_list}

ad_url = 'https://www.kleinanzeigen.de/s-anzeige/ipad-pro-2017-wifi-cellular-too-/2608705598-285-3245'
contact_url = 'https://www.kleinanzeigen.de/s-anbieter-kontaktieren.json'

# Выполняем запрос GET для открытия страницы и получения параметров
response = requests.get(ad_url, headers=headers, cookies=cookies)
response.raise_for_status()
csrf_token = None
# Извлекаем необходимые параметры из HTML страницы с использованием BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')
csrf_token_meta = soup.find('meta', {'name': '_csrf'})
if csrf_token_meta:
    # Extract the CSRF token value from the content attribute
    csrf_token = csrf_token_meta.get('content')
    print(f'csrf_token: {csrf_token}')

ad_id = None
id_tag = soup.find('li', text='Anzeigen-ID')
if id_tag:
    ad_id = id_tag.find_next('li').text
    print(f'ID: {ad_id}')
else:
    print('ID не найден')

session_id = None
session_id_input = soup.find('input', {'name': 'contactPosterWenkseSessionId'})
if session_id_input:
    # Извлекаем значение из атрибута 'value'
    session_id = session_id_input.get('value')
    print(f'Session ID: {session_id}')
else:
    print('Session ID не найден')

# Параметры для запроса POST
data = {
    'adId': ad_id,
    'adType': 'private',
    'message': 'Hello, I like your item',
    'contactName': 'Mary',
    'contactPosterWenkseSessionId': session_id
}
# Выполняем запрос POST для отправки сообщения


new_headers = {
    "Accept-Ch": "sec-ch-ua-model,sec-ch-ua-platform-version,sec-ch-ua-full-version",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Cache-Control": "no-cache, no-store, max-age=0, must-revalidate",
    'Accept-Language': "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'csrf_token': csrf_token
}

try:
    response = requests.post(contact_url, headers=new_headers, cookies=cookies, data=data)
    response.raise_for_status()
    print(response.text)
except requests.exceptions.SSLError as e:
    print(f"SSL Error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Request Error: {e}")
