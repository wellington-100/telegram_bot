from aiohttp import ClientSession
from bs4 import BeautifulSoup
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from tabulate import tabulate



async def comert_bank(update: Update, context: CallbackContext):
    url = "https://www.curs.md/ro/office/comertbank"

    async with ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')

            # Инициализируем переменные для ответов
            response_message = ""

            # Получаем временные интервалы для курсов валют
            time_intervals = soup.find_all('a', {'data-toggle': 'collapse'})
            time_intervals_text = [interval.get_text(strip=True) for interval in time_intervals]
            if time_intervals_text:
                response_message += f"<b>Ratele de schimb: {time_intervals_text[0]}</b>"

            try:
                # Получаем курсы валют
                rows = soup.find_all('tr')
                rates = {}
                for row in rows[1:]:
                    cells = row.find_all('td')
                    if cells and len(cells) >= 5 and cells[0].get_text() in ["USD", "EUR", "RUB", "RON", "UAH", "CAD", "ILS", "CHF", "GBP", "TRY"]:
                        currency = cells[0].get_text()
                        currency_name = cells[1].get_text()
                        buy_rate = cells[3].get_text().replace(",", ".").strip()
                        sell_rate = cells[4].get_text().replace(",", ".").strip()
                        rates[currency] = (currency_name, buy_rate, sell_rate)

                if rates:
                    response_message += f"\n\n<b><code>{'Valuta':<10}{'Cumparare':<10}{'Vanzare':>10}</code></b>\n\n"
                    response_message += "\n".join([f"<b><code>{key:<10} {float(value[1]):^10.2f} {float(value[2]):^10.2f}</code></b>" for key, value in rates.items()])

                # Получаем информацию о банке
                bank_info_div = soup.find('div', class_='bank_info')
                address = bank_info_div.find('h2', string='Adresa').find_next('address').get_text(strip=True)
                map_link = bank_info_div.find('a', class_='btn btn-suggest')['href']

                contact_details_dl = bank_info_div.find('h2', string='Date de contact').find_next('dl', class_='dl-horizontal dl-workhours')
                contact_details = {dt.get_text(strip=True).replace(':', ''): dd.get_text(strip=True) for dt, dd in zip(contact_details_dl.find_all('dt'), contact_details_dl.find_all('dd'))}

                # Получаем рабочие часы
                working_hours_div = bank_info_div.find('h2', string='Orarul de lucru')
                if working_hours_div:
                    working_hours_div = working_hours_div.find_next('div', class_='row')

                if working_hours_div:
                    dl = working_hours_div.find('dl', class_='dl-workhours dl-horizontal')
                else:
                    dl = None

                working_hours_list = []

                if dl:
                    for dt, dd in zip(dl.find_all('dt'), dl.find_all('dd')):
                        day = dt.get_text(strip=True)
                        hours = dd.get_text(strip=True)
                        working_hours_list.append(f"<code><b>{day:<15}</b>{hours:>15}</code>")


                    working_hours = "<b>Orarul de lucru:\n</b>" + '\n'.join(working_hours_list)
                else:
                    working_hours_div = bank_info_div.find('h2', string='Orarul de lucru').find_next('div', class_='row')
                    if working_hours_div:
                        working_hours = "<b>Orarul de lucru:</b>\n" + working_hours_div.get_text(strip=True)
                    else:
                        working_hours = "<b>Orarul de lucru:</b> Информация о рабочих часах не найдена"

                # Собираем всю информацию в одно сообщение
                exchange_name = soup.find('h1').get_text().strip()
                response_message += f"\n\n<b>Informația despre {exchange_name} :</b>\n\n"
                response_message += f"{working_hours}\n\n"
                for key, value in contact_details.items():
                    response_message += f"<b>{key}:</b> {value}\n"
                response_message += f"\n<b>Adresa:\n</b>{address}\n"
                response_message += f"<b>Vezi pe hartă:\n</b>{map_link}"

                # Отправляем сообщение
                await context.bot.send_message(chat_id=update.message.chat_id, text=response_message, parse_mode='HTML')

            except Exception as e:
                print(f"Произошла ошибка: {e}")
                await context.bot.send_message(chat_id=update.message.chat_id, text=f"Произошла ошибка: {e}")