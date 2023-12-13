# Импортируем необходимые библиотеки и модули
from aiohttp import ClientSession     # Асинхронный HTTP-клиент для работы с сетью
from bs4 import BeautifulSoup         # Библиотека для анализа и извлечения данных из HTML/XML
from telegram import Update, ForceReply   # Инструменты Telegram API
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext  # Инструменты для работы с Telegram ботом
from urls import *                   # Предполагаем, что из этого модуля импортируются URL-ы для работы

# Функция-обработчик для извлечения данных с веб-страницы по определенному endpoint
async def fetch_data_handler(update: Update, context: CallbackContext, endpoint: str):
    url = BASE_URLS.get(endpoint)  # Получаем URL по ключу
    if url:
        await fetch_data(update, context, url)  # Если URL найден, запрашиваем данные
    else:
        # Если URL не найден, отправляем ошибку
        await context.bot.send_message(chat_id=update.message.chat_id, text=f"Unknown endpoint: {endpoint}")


# Функция для асинхронного запроса к сайту и обработки ответа
async def fetch_data(update: Update, context: CallbackContext, url: str):
    async with ClientSession() as session:  # Создаем асинхронную сессию для работы с HTTP
        async with session.get(url) as response:  # Отправляем GET запрос
            html = await response.text()  # Получаем содержимое ответа
            soup = BeautifulSoup(html, 'html.parser')  # Парсим HTML
            # Объединяем информацию о курсах и о банке в одно сообщение
            response_message = extract_rate_info(soup) + extract_bank_info(soup)
            try:
                # Отправляем сообщение в Telegram
                await context.bot.send_message(chat_id=update.message.chat_id, text=response_message, parse_mode='HTML')
            except Exception as e:  # Обработка исключений при отправке сообщения
                print(f"Произошла ошибка: {e}")
                await context.bot.send_message(chat_id=update.message.chat_id, text=f"Произошла ошибка: {e}")

# Функция извлечения информации о курсах валют
def extract_rate_info(soup):
    response_message = ""

    time_intervals = soup.find_all('a', {'data-toggle': 'collapse'})
    time_intervals_text = [interval.get_text(strip=True) for interval in time_intervals]
    if time_intervals_text:
        response_message += f"<b>Ratele de schimb: {time_intervals_text[0]}</b>"

    rows = soup.find_all('tr')
    rates = extract_currency_rates(rows)
    
    if rates:
        response_message += format_currency_rates(rates)
    
    return response_message

# Функция для извлечения информации о курсах валют из таблицы
def extract_currency_rates(rows):
    rates = {}
    for row in rows[1:]:
        cells = row.find_all('td')
        if cells and len(cells) >= 5 and cells[0].get_text() in ["USD", "EUR", "RUB", "RON", "UAH", "CAD", "ILS", "CHF", "GBP", "TRY", "AED", "AUD", "BYN", "CNY", "CZK", "HUF", "JPY", "SEK", "PLN", "DKK", "HRK", "NOK", ]:
            currency = cells[0].get_text()
            currency_name = cells[1].get_text()
            buy_rate = cells[3].get_text().replace(",", ".").strip()
            sell_rate = cells[4].get_text().replace(",", ".").strip()
            rates[currency] = (currency_name, buy_rate, sell_rate)
    return rates

# Функция для форматирования информации о курсах валют
def format_currency_rates(rates):
    response_message = f"\n\n<b><code>{'Valuta':<10}{'Cumparare':<10}{'Vanzare':>10}</code></b>\n\n"
    response_message += "\n".join([f"<b><code>{key:<10} {float(value[1]):^10.2f} {float(value[2]):^10.2f}</code></b>" for key, value in rates.items()])
    return response_message

# Функция для извлечения информации о банке
def extract_bank_info(soup):
    response_message = ""
    
    bank_info_div = soup.find('div', class_='bank_info')
    exchange_name = soup.find('h1').get_text().strip()

    # Извлекаем информацию о банке
    address = bank_info_div.find('h2', string='Adresa').find_next('address').get_text(strip=True)
    map_link = bank_info_div.find('a', class_='btn btn-suggest')['href']

    contact_details_dl = bank_info_div.find('h2', string='Date de contact').find_next('dl', class_='dl-horizontal dl-workhours')
    contact_details = {dt.get_text(strip=True).replace(':', ''): dd.get_text(strip=True) for dt, dd in zip(contact_details_dl.find_all('dt'), contact_details_dl.find_all('dd'))}
    
    # Извлекаем рабочие часы
    working_hours_div = bank_info_div.find('h2', string='Orarul de lucru')
    if working_hours_div:
        working_hours_div = working_hours_div.find_next('div', class_='row')

    if working_hours_div:
        dl = working_hours_div.find('dl', class_='dl-workhours dl-horizontal')
    else:
        dl = None

    working_hours_list = []
#################
    if dl:
        working_hours_list = []
        for dt, dd in zip(dl.find_all('dt'), dl.find_all('dd')):
            day = dt.get_text(strip=True)
            hours = dd.get_text(strip=True)

            # Удаляем часть строки, начиная с " (pauza" (если она найдена)
            hours = hours.split(' (pauza')[0]

            working_hours_list.append((day, hours))

        # Проверка, если информация о времени работы отсутствует для всех дней
        if all(hours.strip() == "-" for day, hours in working_hours_list):
            working_hours = "<b>Orarul de lucru:</b> Nu există informație referitoare la orar"
        else:
            working_hours = "<b>Orarul de lucru:\n</b>" + '\n'.join(f"<code><b>{day:<15}</b>{hours:>15}</code>" for day, hours in working_hours_list)
    else:
        if working_hours_div:
            working_hours = "<b>Orarul de lucru:</b>\n" + working_hours_div.get_text(strip=True)
        else:
            working_hours = "<b>Orarul de lucru:</b> Информация о рабочих часах не найдена"
   
    # Собираем всю информацию в одно сообщение
    response_message += f"\n\n<b>Informația despre {exchange_name} :</b>\n\n"
    response_message += f"{working_hours}\n\n"
    for key, value in contact_details.items():
        response_message += f"<b>{key}:</b> {value}\n"
    response_message += f"\n<b>Adresa:\n</b>{address}\n"
    response_message += f"<b>Vezi pe hartă:\n</b>{map_link}"

    return response_message
#

# Функция-обработчик команд от пользователя
async def command_handler(update: Update, context: CallbackContext):
    command = update.message.text.lstrip("/").lower()
    if command in BASE_URLS:
        await fetch_data_handler(update, context, command)
    else:
        await context.bot.send_message(chat_id=update.message.chat_id, text=f"Unsupported command: {command}")













