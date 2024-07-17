"""Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/ и извлечь
информацию о всех книгах на сайте во всех категориях: название, цену, количество
товара в наличии (In stock (19 available)) в формате integer, описание.
Затем сохранить эту информацию в JSON-файле."""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

# Базовый URL сайта
base_url = "http://books.toscrape.com/catalogue/"

# Функция для получения HTML кода страницы
def get_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

# Функция для извлечения информации о книге со страницы
def get_book_info(book_url):
    html = get_html(book_url)
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('h1').text
    price = soup.find('p', class_='price_color').text[2:]
    stock = soup.find('p', class_='instock availability').text.strip().split()[-2]
    stock = int(stock)
    description = soup.find('meta', {'name': 'description'})['content'].strip()
    return {
        'title': title,
        'price': float(price),
        'stock': stock,
        'description': description
    }

# Функция для извлечения ссылок на все книги со страницы категории
def get_books_from_category(category_url):
    books = []
    html = get_html(category_url)
    soup = BeautifulSoup(html, 'html.parser')
    for book in soup.find_all('h3'):
        book_url = base_url + book.find('a')['href'].replace('../../../', '')
        books.append(get_book_info(book_url))
    return books

# Функция для получения ссылок на все категории
def get_all_categories():
    url = "http://books.toscrape.com/"
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    categories = []
    for category in soup.find('div', class_='side_categories').find_all('a'):
        category_name = category.text.strip()
        if category_name != 'Books':
            category_url = base_url + category['href']
            categories.append((category_name, category_url))
    return categories

# Главная функция
def main():
    all_books = []
    categories = get_all_categories()
    for category_name, category_url in categories:
        print(f"Scraping category: {category_name}")
        books = get_books_from_category(category_url)
        all_books.extend(books)

    # Сохранение данных в JSON файл
    with open('books.json', 'w') as f:
        json.dump(all_books, f, indent=4)

    # Создание pandas DataFrame и вывод таблицы
    df = pd.DataFrame(all_books)
    print(df)

if __name__ == "__main__":
    main()
