from aiohttp import ClientSession
from bs4 import BeautifulSoup
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import re
import aioredis
import asyncio
from datetime import datetime, time
import json
from currency_flags import currency_flags
from urls import urls




async def get_basic_rates(currency: str) -> str:
    url = "https://www.curs.md/ro/curs_valutar_banci"
    
    async with ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return "Ошибка загрузки страницы"
            html = await response.text()

    soup = BeautifulSoup(html, 'html.parser')

    # Получение даты
    date_value = soup.find('input', {'id': 'BanksCotDate'})['value']
    date_obj = datetime.strptime(date_value, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%d.%m.%Y")

    # Находим таблицу с данными
    table = soup.find('table', id='tabelBankValute')
    rows = table.find_all('tr')[1:]  # Исключение заголовка таблицы

    results = []
    exclusions = ["SRL", "CSV", "Tighina", "Filiala Kiev", "BNM", "Bancă", "\""]
    replacements = {
        "Filiala 1": "1",
        "Filiala 2": "2",
        "Filiala 3": "3",
        "Filiala 4": "4",
        "Filiala 7": "7",
        "Filiala 9": "9",
        "Sucursala 1": "1",
        "Sucursala 2": "2",
        "Sucursala 3": "3",
        "Sucursala 4": "4",
        "Sucursala 5": "5",
        # Добавьте другие замены по необходимости
    }    
    for row in rows:
        bank_name_cell = row.find('td', class_='bank_name')
        if bank_name_cell is None:
            continue  # Пропустить эту строку, если элемент не найден
        bank_name = row.find('td', class_='bank_name').get_text(strip=True)
        # Применение замен
        for old, new in replacements.items():
            bank_name = bank_name.replace(old, new)

        # Удаление исключений
        for exclusion in exclusions:
            bank_name = bank_name.replace(exclusion, "")

        bank_name = re.sub(r'\(.*?\)', '', bank_name).strip()
        if "Banca Nationala" in bank_name:
            continue

        cols = row.find_all('td', class_=f'column-{currency}')

        if cols:
            cump = cols[0].text.strip().replace(",", ".")
            vanz = cols[1].text.strip().replace(",", ".")

            # Преобразование в float и форматирование
            try:
                cump_float = float(cump)
                vanz_float = float(vanz)
                results.append(f"<pre><b>{bank_name:20}</b> {cump_float:.2f}  {vanz_float:.2f}</pre>")
            except ValueError:
                continue

    if not results:
        return f"Нет данных по валюте {currency}."

   
    selected_currency_flag = currency_flags.get(currency, "")
    header = f"<b>RATE DE SCHIMB VALUTAR: {formatted_date or 'Lipsă dată'}\n{selected_currency_flag} {currency} / MDL {currency_flags['MDL']}</b>\n\n"
    return header + '\n'.join(results)

async def custom_basic_rates(update: Update, context: CallbackContext) -> None:
    currency = update.message.text[1:].upper()
    rates_message = await get_basic_rates(currency)
    await update.message.reply_text(rates_message, parse_mode="HTML")







# async def get_basic_rates(currency_code: str) -> dict:
#     url = "https://www.curs.md/ro/curs_valutar_banci"
#     all_data = {}
#     formatted_date = None

#     async with ClientSession() as session:
#         async with session.get(url) as response:
#             html = await response.text()
#             soup = BeautifulSoup(html, 'html.parser')

#             # Извлечение и форматирование даты
#             date_elem = soup.find('input', {'id': 'BanksCotDate'})
#             if date_elem:
#                 date_value = date_elem.get('value')
#                 try:
#                     date_obj = datetime.strptime(date_value, "%Y-%m-%d")
#                     formatted_date = date_obj.strftime("%d.%m.%Y")
#                 except ValueError:
#                     return "Ошибка формата даты"
#             print(f"Дата: {formatted_date}")

#             table = soup.find('table', {'id': 'tabelBankValute'})
#             if not table:
#                 return "Ошибка: таблица курсов не найдена"

#             # Считываем заголовки столбцов для определения порядка валют
#             headers = table.find('tr').find_all('td')[1:]  # Пропускаем первый столбец с названием банка
#             currency_order = [header.get('class')[0].split('-')[1] for header in headers if 'column-auto' not in header.get('class')[0]]

#             print(f"Порядок валют: {currency_order}")

#             for row in table.find_all('tr')[1:]:
#                 cells = row.find_all('td')
#                 if not cells or len(cells) < 2:
#                     print("Строка без данных или с недостаточным количеством ячеек")
#                     continue
#                 bank_name = cells[0].get_text(strip=True)
#                 print(f"Обрабатываем банк: {bank_name}")

#                 currency_data = []
#                 for cell in cells[1:]:
#                     if 'column-auto' not in cell.get('class', []):
#                         currency_data.append(cell.get_text(strip=True))

#                 # Убедимся, что количество элементов в currency_data соответствует ожидаемому
#                 if len(currency_data) != len(currency_order) * 2:
#                     print(f"Недостаточное количество данных для валют в банке {bank_name}")
#                     continue

#                 for i in range(0, len(currency_order) * 2, 2):
#                     currency_code = currency_order[i // 2]
#                     cump_rate = currency_data[i].replace(",", ".")
#                     vanz_rate = currency_data[i + 1].replace(",", ".")

#                     if cump_rate and vanz_rate and cump_rate != '-' and vanz_rate != '-':
#                         cump_float = float(cump_rate)
#                         vanz_float = float(vanz_rate)
#                         if currency_code not in all_data:
#                             all_data[currency_code] = []
#                         all_data[currency_code].append({
#                             "exchanger_name": bank_name,
#                             "cump": f'{cump_float:.2f}',
#                             "vanz": f'{vanz_float:.2f}',
#                             "cump_float": cump_float,
#                             "vanz_float": vanz_float
#                         })
#                 print(f"Обработанные данные для {bank_name}: {all_data.get(currency_code, 'Нет данных')}")

#     if currency_code in all_data:
#         data = all_data[currency_code]
#         results = [f"{item['exchanger_name']}: {item['cump']} / {item['vanz']}" for item in data]
#         header = f"<b>RATE DE SCHIMB VALUTAR: {formatted_date or 'Lipsă dată'}\n{currency_code}</b>\n"
#         return header + '\n'.join(results)
#     else:
#         return f"Нет данных по валюте {currency_code}."










async def get_exotic_rates(currencies: list, sort_key: str = 'cump', reverse: bool = True) -> dict:
    results = []
    all_data = {}
    date = None  # Задайте начальное значение для date
    for url in urls:
        async with ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                h1_tag = soup.find('h1')
                if h1_tag is not None:
                    exchanger_name = h1_tag.text.strip()
                    exclusions = ["SRL", "CSV", "Tighina", "Filiala Kiev", "\""]
                    replacements = {
                        "Filiala 1": "F-1",
                        "Filiala 2": "F-2",
                        "Filiala 3": "F-3",
                        "Filiala 4": "F-4",
                        "Filiala 7": "F-7",
                        "Filiala 9": "F-9",
                        "Sucursala 1": "S-1",
                        "Sucursala 2": "S-2",
                        "Sucursala 3": "S-3",
                        "Sucursala 4": "S-4",
                        "Sucursala 5": "S-5",
                        # Добавьте другие замены по необходимости
                    }
                    for old, new in replacements.items():
                        exchanger_name = exchanger_name.replace(old, new)
                    for exclusion in exclusions:
                        exchanger_name = exchanger_name.replace(exclusion, "")
                        exchanger_name = re.sub(r'\(.*?\)', '', exchanger_name).strip()
                    if exchanger_name:
                        date = soup.find('input', {'id': 'BankCotDate'})['value']
                        if date:
                            # Преобразование формата даты из 'YYYY-MM-DD' в 'DD.MM.YYYY'
                            date_obj = datetime.strptime(date, "%Y-%m-%d")
                            formatted_date = date_obj.strftime("%d.%m.%Y")
                        else:
                            return "Ошибка при извлечении даты"
                        table = soup.find('table', class_='table table-hover')
                        rows = table.find_all('tr')[1:]

                    for row in rows:
                        cols = row.find_all('td')
                        valuta = cols[0].text.strip()
                        cump = cols[3].text.strip().replace(",", ".")
                        vanz = cols[4].text.strip().replace(",", ".")
                        try:
                            cump_float = float(cump)
                            vanz_float = float(vanz)  # Преобразование vanz в float
                        except ValueError:
                            continue

                        if valuta not in all_data:
                            all_data[valuta] = []
                        
                        all_data[valuta].append({
                            "exchanger_name": exchanger_name,
                            "cump": f'{cump_float:.2f}',
                            "vanz": f'{vanz_float:.2f}',
                            "cump_float": cump_float,
                            "vanz_float": vanz_float
                    })

                    else:
                        exchanger_name = "Не найдено"
    formatted_results = {}
    for currency, data in all_data.items():
        if data:
            # Сортировка данных для каждой валюты
            sorted_data = sorted(data, key=lambda x: x['cump_float'], reverse=reverse)

            # Формирование строки результатов для каждой валюты
            results = [f"<pre><b>{item['exchanger_name']:20}</b> {item['cump']:>5}  {item['vanz']:5}</pre>" for item in sorted_data]
            selected_currency_flag = currency_flags.get(currency, "")
            header = f"<b>RATE DE SCHIMB VALUTAR: {formatted_date or 'Lipsă dată'}\n{selected_currency_flag} {currency} / MDL {currency_flags['MDL']}</b>\n\n"
            formatted_results[currency] = header + '\n'.join(results)
        else:
            # Сообщение о том, что данных по данной валюте нет
            formatted_results[currency] = f"<b>Нет данных по валюте {currency}.</b>"

    return formatted_results


async def custom_exotic_rates(update: Update, context: CallbackContext, currency: str, sort_key: str, reverse: bool = False) -> None:
    rate_message = await get_exotic_rates(currency, sort_key, reverse)
    await update.message.reply_text(rate_message, parse_mode="HTML")

####################################################################################################################################


# Создание подключения к Redis (глобально)
redis_pool = None

async def create_redis_connection():
    global redis_pool
    if not redis_pool:
        print("Создание нового соединения с Redis...")
        redis_pool = await aioredis.create_redis_pool('redis://localhost')
    else:
        print("Использование существующего соединения с Redis...")
    return redis_pool

# Функция для обновления кэша
async def update_cache():
    currency_codes = ['AED', 'AUD', 'BGN', 'BYN', 'CNY', 'CZK', 'DKK', 'HRK', 'HUF', 'ILS', 'JPY', 'NOK', 'PLN', 'SEK']
    all_rates = await get_exotic_rates(currency_codes)
    
    redis = await create_redis_connection()
    for currency, data in all_rates.items():
        await redis.set(f'currency_{currency}', json.dumps(data))

    print("Кэш для всех валют успешно обновлен.")


async def scheduled_requests():
    while True:
        print("Проверка времени для запланированного обновления кэша...")
        now = datetime.now()
        if time(17, 17) <= now.time() <= time(19, 17):
            for currency in ['AED', 'AUD', 'BGN', 'BYN', 'CNY', 'CZK', 'DKK', 'HRK', 'HUF', 'ILS', 'JPY', 'NOK', 'PLN', 'SEK']:
                await update_cache(currency)
        await asyncio.sleep(60)

async def get_cached_rate(currency: str):
    print(f"Получение курса для {currency} из кэша...")
    redis = await create_redis_connection()
    cached_data = await redis.get(f'currency_{currency}')
    if cached_data:
        print(f"Найден кэш для {currency}.")
        return json.loads(cached_data)
    else:
        print(f"Кэш для {currency} пуст или устарел.")
        return None

async def cached_rate(update: Update, context: CallbackContext):
    currency = update.message.text[1:].upper()
    print(f"Запрос кэшированного курса для {currency}...")
    rate_message = await get_cached_rate(currency)
    if rate_message:
        await update.message.reply_text(rate_message, parse_mode="HTML")
    else:
        await update.message.reply_text("Кэш пуст или устарел.", parse_mode="HTML")


async def force_update(update: Update, context: CallbackContext):
    currency_codes = ['AED', 'AUD', 'BGN', 'BYN', 'CNY', 'CZK', 'DKK', 'HRK', 'HUF', 'ILS', 'JPY', 'NOK', 'PLN', 'SEK']
    all_rates = await get_exotic_rates(currency_codes)
    
    redis = await create_redis_connection()
    for currency, data in all_rates.items():
        await redis.set(f'currency_{currency}', json.dumps(data))

    await update.message.reply_text("Кэш для всех валют был принудительно обновлен.", parse_mode="HTML")


#########################################




async def get_bnm_rate() -> str:
    url = "https://www.curs.md/ro/curs_valutar/oficial"
    async with ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            
            date_elem = soup.find('input', {'id': 'OfficialCotDate'})
            if date_elem:
                date_value = date_elem.get('value')
                try:
                    date_obj = datetime.strptime(date_value, "%Y-%m-%d")
                    formatted_date = date_obj.strftime("%d.%m.%Y")
                except ValueError:
                    return "Ошибка формата даты"
            else:
                return "Ошибка при извлечении даты"

            table = soup.find('table', {'id': 'tabelValute'})
            if not table:
                return "Ошибка: таблица курсов не найдена"

            rates = {}
            for row in table.find_all('tr')[1:]:  # Пропускаем заголовок таблицы
                cells = row.find_all('td')
                if len(cells) >= 3:
                    currency = cells[0].get_text(strip=True)
                    rate = cells[2].get_text(strip=True)

                    change_value = cells[3].get_text().split()[0]
                    arrow_up = "▲"  # Стрелка вверх
                    arrow_down = "▼"  # Стрелка вниз
                    arrow_stable = "⚊"  # Тире для стабильности

                    if "-" in change_value:
                        change_direction = arrow_down
                    elif change_value == "0" or change_value == "0,0000":
                        change_direction = arrow_stable  # Использование тире для обозначения отсутствия изменений
                    else:
                        change_direction = arrow_up

                    change_full = f"{change_value} {change_direction}"
                    # Получаем флаг для валюты
                    flag = currency_flags.get(currency, "")
                    # Формируем строку с информацией о валюте, включая флаг
                    rates[currency] = {"flag": flag, "rate": rate, "change": change_full}

    # Формирование итогового сообщения
    if rates:
        message_lines = [f" <b>CURS OFICIAL BNM {currency_flags['MDL']} pentru {formatted_date}</b>\n"]

        for key, data in rates.items():
            message_lines.append(f"{data['flag']}<code> {key:<7} {data['rate']:10} {data['change']:>10}</code>")
        return "\n".join(message_lines)
    else:
        return "Данные о курсах валют не найдены"


async def bnm_rate(update: Update, context: CallbackContext) -> None:
    rate_message = await get_bnm_rate()
    await update.message.reply_text(rate_message, parse_mode="HTML")




# async def get_bnm_rate() -> str:
#     url = "https://www.curs.md/ro/curs_valutar_banci"
#     async with ClientSession() as session:
#         async with session.get(url) as response:
#             html = await response.text()
#             soup = BeautifulSoup(html, 'html.parser')
            
#             date_elem = soup.find('input', {'id': 'BoxCotDate'})
#             if date_elem:
#                 # Извлечение значения атрибута 'value'
#                 date_value = date_elem.get('value')

#                 # Преобразование формата даты из 'YYYY-MM-DD' в 'DD.MM.YYYY'
#                 try:
#                     date_obj = datetime.strptime(date_value, "%Y-%m-%d")
#                     formatted_date = date_obj.strftime("%d.%m.%Y")
#                 except ValueError:
#                     return "Ошибка формата даты"
#             else:
#                 return "Ошибка при извлечении даты"

#             rows = soup.find_all('tr')
#             rates = {}
#             for row in rows:
#                 cells = row.find_all('td')
#                 if cells and len(cells) >= 3 and cells[1].get_text() in ["USD", "EUR", "RUB", "RON", "UAH", "GBP", "CHF", "TRY", "CAD"]:
#                     currency = cells[1].get_text()
#                     rate = cells[2].get_text().replace(" Lei", "")
                    
#                     change_value = cells[3].get_text().split()[0] 

#                     arrow_up = "▲"  # ↑
#                     arrow_down = "▼"  # ↓
                    
#                     if "-" in change_value:
#                         change_direction = arrow_down
#                     elif change_value == "0" or change_value == "0,0000":
#                         change_direction = ""
#                     else:
#                         change_direction = arrow_up

#                     change_full = f"{change_value} {change_direction}"
                    
#                     rates[currency] = {"rate": rate, "change": change_full}
#             if rates:
#                 message_lines = [f"<b>Cursul Oficial BNM pentru {formatted_date}</b>\n"]
                
#                 for key, data in rates.items():
#                     message_lines.append(f"<code>{key:<10} {data['rate']:10} {data['change']:>10}</code>")
#                 return "\n".join(message_lines)

# async def bnm_rate(update: Update, context: CallbackContext) -> None:
#     rate_message = await get_bnm_rate()
#     await update.message.reply_text(rate_message, parse_mode="HTML")
#########