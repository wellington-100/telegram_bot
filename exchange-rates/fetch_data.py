
from aiohttp import ClientSession    
from bs4 import BeautifulSoup        
from telegram import Update, ForceReply  
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext 
from urls import * 
from currency_info import currency_flags, currency_codes 


async def fetch_data_handler(update: Update, context: CallbackContext, endpoint: str):
    url = BASE_URLS.get(endpoint)  
    if url:
        await fetch_data(update, context, url) 
    else:

        await context.bot.send_message(chat_id=update.message.chat_id, text=f"Unknown endpoint: {endpoint}")

async def fetch_data(update: Update, context: CallbackContext, url: str):
    async with ClientSession() as session: 
        async with session.get(url) as response:  
            html = await response.text()  
            soup = BeautifulSoup(html, 'html.parser')
            response_message = extract_rate_info(soup) + extract_bank_info(soup)
            try:
                await context.bot.send_message(chat_id=update.message.chat_id, text=response_message, parse_mode='HTML')
            except Exception as e:  
                print(f"Произошла ошибка: {e}")
                await context.bot.send_message(chat_id=update.message.chat_id, text=f"Произошла ошибка: {e}")

def extract_rate_info(soup):
    response_message = ""

    time_intervals = soup.find_all('a', {'data-toggle': 'collapse'})
    time_intervals_text = [interval.get_text(strip=True) for interval in time_intervals]
    if time_intervals_text:
        response_message += f"<b>Ratele de schimb: {time_intervals_text[0]}</b>"

    rows = soup.find_all('tr')
    rates = extract_currency_rates(rows, currency_codes)
    
    if rates:
        response_message += format_currency_rates(rates)
    
    return response_message

def extract_currency_rates(rows, currency_codes):
    rates = {}
    for row in rows[1:]:
        cells = row.find_all('td')
        if cells and len(cells) >= 5 and cells[0].get_text() in currency_codes:
            currency = cells[0].get_text()
            currency_name = cells[1].get_text()
            buy_rate = cells[3].get_text().replace(",", ".").strip()
            sell_rate = cells[4].get_text().replace(",", ".").strip()
            rates[currency] = (currency_name, buy_rate, sell_rate)
    return rates

def format_currency_rates(rates):
    response_message = f"\n\n<b><code>{'Valuta':<10}{'Cumparare':<10}{'Vanzare':>10}</code></b>\n\n"
    for key, value in rates.items():
        flag = currency_flags.get(key, "")  # Получение флага для валюты
        response_message += f"{flag}<code> {key:<8} {float(value[1]):^10.2f} {float(value[2]):^10.2f}</code>\n"
    return response_message

def extract_bank_info(soup):
    response_message = ""
    
    bank_info_div = soup.find('div', class_='bank_info')
    if not bank_info_div:
        return "Bank info not found."

    h1_tag = soup.find('h1')
    exchange_name = h1_tag.get_text().strip() if h1_tag else "Name not found"

    address = bank_info_div.find('h2', string='Adresa')
    address = address.find_next('address').get_text(strip=True) if address else "Address not found"

    map_link = bank_info_div.find('a', class_='btn btn-suggest')
    map_link = map_link['href'] if map_link else "Map link not found"

    contact_details_dl = bank_info_div.find('h2', string='Date de contact')
    if contact_details_dl:
        contact_details_dl = contact_details_dl.find_next('dl', class_='dl-horizontal dl-workhours')
        contact_details = {dt.get_text(strip=True).replace(':', ''): dd.get_text(strip=True) 
                           for dt, dd in zip(contact_details_dl.find_all('dt'), contact_details_dl.find_all('dd'))}
    else:
        contact_details = "Contact details not found"

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

            hours = hours.split(' (pauza')[0]

            working_hours_list.append((day, hours))

        if all(hours.strip() == "-" for day, hours in working_hours_list):
            working_hours = "<b>Orarul de lucru:</b> Nu există informație referitoare la orar"
        else:
            working_hours = "<b>Orarul de lucru:\n</b>" + '\n'.join(f"<code><b>{day:<15}</b>{hours:>15}</code>" for day, hours in working_hours_list)
    else:
        if working_hours_div:
            working_hours = "<b>Orarul de lucru:</b>\n" + working_hours_div.get_text(strip=True)
        else:
            working_hours = "<b>Orarul de lucru:</b> Информация о рабочих часах не найдена"

    response_message += f"\n\n<b>Informația despre {exchange_name} :</b>\n\n"
    response_message += f"{working_hours}\n\n"
    for key, value in contact_details.items():
        response_message += f"<b>{key}:</b> {value}\n"
    response_message += f"\n<b>Adresa:\n</b>{address}\n"
    response_message += f"<b>Vezi pe hartă:\n</b>{map_link}"

    return response_message

async def command_handler(update: Update, context: CallbackContext):
    command = update.message.text.lstrip("/").lower()
    if command in BASE_URLS:
        await fetch_data_handler(update, context, command)
    else:
        await context.bot.send_message(chat_id=update.message.chat_id, text=f"Comandă inexistentă: {command}")













