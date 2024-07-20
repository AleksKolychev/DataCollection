"""Установите MongoDB на локальной машине, а также зарегистрируйтесь в онлайн-сервисе. 
https://www.mongodb.com/ https://www.mongodb.com/products/compass
Загрузите данные который вы получили на предыдущем уроке путем скрейпинга сайта с помощью Buautiful Soup в MongoDB 
и создайте базу данных и коллекции для их хранения.
Поэкспериментируйте с различными методами запросов.
."""

from pymongo import MongoClient
import json
client = MongoClient('localhost', 27017)
db = client['books']
book_info = db['book_info']
with open('books.json', 'r') as file:
    books_json = json.load(file)
for book in books_json:
    book_info.insert_one(book)
books_data = book_info.find()

# Найдём общее количество документов
book_count = book_info.count_documents({})
print(f'Число записей в базе данных: {book_count}')

# Найдём книги, у которых цена более чем 20
price_gte_20 = book_info.count_documents(filter={'price': {'$gte': 20.00}})
print(f'Количество книг дороже 10.0: {price_gte_20}')


# Найдём количество книг, которых на складе не более 15
stock_lt_15 = book_info.count_documents(filter={'stock': {'$lt': 15}})
print(f'Количество книг, которых на складе меньше 15: {stock_lt_15}')

# Найдём количество книг, которые начинаются на букву 'F'
projection = {'_id': 0, 'book_name': 1}
books_starting_with_f = book_info.find({ 'book_name': { '$regex': '^F', '$options': 'i' }}, projection)
for book in books_starting_with_f:
    print(book)  
