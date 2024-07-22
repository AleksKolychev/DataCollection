"""Выберите веб-сайт с табличными данными, который вас интересует.
Напишите код Python, использующий библиотеку requests для отправки HTTP GET-запроса на сайт и получения HTML-содержимого страницы.
Выполните парсинг содержимого HTML с помощью библиотеки lxml, чтобы извлечь данные из таблицы.
Сохраните извлеченные данные в CSV-файл с помощью модуля csv.
Ваш код должен включать следующее:
-Строку агента пользователя в заголовке HTTP-запроса, чтобы имитировать веб-браузер и избежать блокировки сервером.
-Выражения XPath для выбора элементов данных таблицы и извлечения их содержимого.
-Обработка ошибок для случаев, когда данные не имеют ожидаемого формата.
-Комментарии для объяснения цели и логики кода.
"""


# Импорт необходимых библиотек
import requests
from lxml import html
import pandas as pd
from pymongo import MongoClient
import time

# Определение целевого URL
url = "https://worldathletics.org/records/all-time-toplists/sprints/100-metres/outdoor/women/senior"

# Отправка HTTP GET запроса на целевой URL с пользовательским заголовком User-Agent
response = requests.get(url, headers = {
   'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})

# Парсинг HTML-содержимого ответа с помощью библиотеки lxml
tree = html.fromstring(response.content)
# Использование выражения XPath для выбора всех строк таблицы в пределах таблицы с классом 'records-table'
table_rows = tree.xpath("//table[@class='records-table']/tbody/tr")

data = []
for row in table_rows:
    columns = row.xpath(".//td/text()")
    data.append({
        'rank': columns[0].strip(),
        'mark': columns[1].strip(),
        'wind': columns[2].strip(),
        'competitor': row.xpath(".//td[4]/a/text()")[0].strip(),
        'nat': columns[7].strip(),
        'pos': columns[8].strip(),
        'venue': columns[9].strip(),
        'date': columns[10].strip(),
        'resultscore': columns[11].strip()
    })
print(data)

df = pd.DataFrame(data)
print('DataFrame:\n', df)

df.to_csv('saved_ratings.csv', index=False)