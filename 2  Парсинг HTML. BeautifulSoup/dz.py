"""Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/ и извлечь
информацию о всех книгах на сайте во всех категориях: название, цену, количество
товара в наличии (In stock (19 available)) в формате integer, описание.
Затем сохранить эту информацию в JSON-файле."""

# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import json

# # Базовый URL сайта
# base_url = "http://books.toscrape.com/catalogue/"

# # Функция для получения HTML кода страницы
# def get_html(url):
#     response = requests.get(url)
#     response.raise_for_status()
#     return response.text

# # Функция для извлечения информации о книге со страницы
# def get_book_info(book_url):
#     html = get_html(book_url)
#     soup = BeautifulSoup(html, 'html.parser')
#     title = soup.find('h1').text
#     price = soup.find('p', class_='price_color').text[2:]
#     stock = soup.find('p', class_='instock availability').text.strip().split()[-2]
#     stock = int(stock)
#     description = soup.find('meta', {'name': 'description'})['content'].strip()
#     return {
#         'title': title,
#         'price': float(price),
#         'stock': stock,
#         'description': description
#     }

# # Функция для извлечения ссылок на все книги со страницы категории
# def get_books_from_category(category_url):
#     books = []
#     html = get_html(category_url)
#     soup = BeautifulSoup(html, 'html.parser')
#     for book in soup.find_all('h3'):
#         book_url = base_url + book.find('a')['href'].replace('../../../', '')
#         books.append(get_book_info(book_url))
#     return books

# # Функция для получения ссылок на все категории
# def get_all_categories():
#     url = "http://books.toscrape.com/"
#     html = get_html(url)
#     soup = BeautifulSoup(html, 'html.parser')
#     categories = []
#     for category in soup.find('div', class_='side_categories').find_all('a'):
#         category_name = category.text.strip()
#         if category_name != 'Books':
#             category_url = base_url + category['href']
#             categories.append((category_name, category_url))
#     return categories

# # Главная функция
# def main():
#     all_books = []
#     categories = get_all_categories()
#     for category_name, category_url in categories:
#         print(f"Scraping category: {category_name}")
#         books = get_books_from_category(category_url)
#         all_books.extend(books)

#     # Сохранение данных в JSON файл
#     with open('books.json', 'w') as f:
#         json.dump(all_books, f, indent=4)

#     # Создание pandas DataFrame и вывод таблицы
#     df = pd.DataFrame(all_books)
#     print(df)

# if __name__ == "__main__":
#     main()



import requests
from bs4 import BeautifulSoup
from time import sleep
import json
from concurrent.futures import ThreadPoolExecutor


class BookScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
        self.book_info_list = []

    def get_url(self, count):
        url = f"https://books.toscrape.com/catalogue/page-{count}.html"
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")
        data = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        for link in data:
            book_url = "https://books.toscrape.com/catalogue/" + link.find("a").get("href")
            yield book_url

    def scrape_book_info(self, book_url):
        try:
            book_info = {}
            response = requests.get(book_url, headers=self.headers)
            sleep(1)
            soup = BeautifulSoup(response.text, "html.parser")
            data = soup.find("div", class_="content")
            book_name = data.find("h1").text
            price = float(soup.find("p", class_="price_color").text[2:])
            description = soup.find("meta", attrs={"name": "description"})["content"].strip()
            stock = int(soup.find("p", class_="instock availability").text.split()[2][1:])
            book_url_img = "https://books.toscrape.com/" + data.find("img").get("src").replace("../", "")
            book_info = {"book_name": book_name, "price": price, "description": description, "stock": stock,
                         "book_url": book_url}
            self.book_info_list.append(book_info)
            print(book_info)
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def scrape_books(self):
        with ThreadPoolExecutor(max_workers=5) as executor:
            for count in range(1, 51):
                urls = self.get_url(count)
                executor.map(self.scrape_book_info, urls)

        with open('books.json', 'w') as f:
            json.dump(self.book_info_list, f, indent=4)


if __name__ == "__main__":
    scraper = BookScraper()
    scraper.scrape_books()