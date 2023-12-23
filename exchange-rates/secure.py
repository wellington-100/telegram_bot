from aiohttp import ClientSession
from bs4 import BeautifulSoup
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from basil_testing_bot.fetch_data import *


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Я ваш простой бот.')

async def haha(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Что с тобой?')

    
###################################### bnm  ############################################
async def get_bnm_rate() -> str:
    url = "https://www.curs.md/ro/office/bnm"
    async with ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            
            # Извлекаем дату
            date_elem = soup.find('input', {'id': 'BoxCotDate'})
            if not date_elem:
                return "Ошибка при извлечении даты"
            date_value = date_elem.get('value')

            # Извлекаем все строки и найдем те, которые содержат информацию о курсах
            rows = soup.find_all('tr')
            rates = {}
            for row in rows:
                cells = row.find_all('td')
                if cells and len(cells) >= 3 and cells[1].get_text() in ["USD", "EUR", "RUB", "RON", "UAH"]:
                    currency = cells[1].get_text()
                    rate = cells[2].get_text().replace(" Lei", "")
                    
                    # Извлекаем значение изменения
                    change_value = cells[3].get_text().split()[0]  # Получаем "0,0269", "-0,0269" или "0"

                    arrow_up = "\u2191"  # ↑
                    arrow_down = "\u2193"  # ↓
                    
                    if "-" in change_value:
                        change_direction = arrow_down
                    elif change_value == "0" or change_value == "0,0000":
                        change_direction = ""
                    else:
                        change_direction = arrow_up

                    change_full = f"{change_value} {change_direction}"
                    # Таким образом, если значение не изменилось, будет отображаться просто число без стрелок. Если значение увеличилось, будет отображаться число и стрелка вверх. Если значение уменьшилось, будет отображаться число и стрелка вниз.

                    rates[currency] = {"rate": rate, "change": change_full}
            if rates:
                message_lines = [f"Cursul Oficial BNM pentru: {date_value}"]
                for key, data in rates.items():
                    message_lines.append(f"{key}: {data['rate']} ({data['change']})")
                return "\n".join(message_lines)
            # Оставшийся код без изменений


async def bnm_rate(update: Update, context: CallbackContext) -> None:
    rate_message = await get_bnm_rate()
    await update.message.reply_text(rate_message)



####################################### CLIO    ######################################

async def clio(update: Update, context: CallbackContext):
    command_list = update.message.text.split(' ')
    if len(command_list) < 2:
        await update.message.reply_text('Alegeți Filiala:\n/cliocsv(Central),\n/clio1(Filiala 1)')
        return
    command = command_list[1]
    
    if command == 'cliocsv':
        await clio_csv(update, context)
    elif command == 'clio1':
        await clio_1(update, context)
    else:
        await update.message.reply_text('Неизвестная подкоманда.')



################################ clio csv   ###############################################

async def clio_csv(update: Update, context: CallbackContext):
    url = "https://www.curs.md/ro/office/clio"

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


################################ clio    ###############################################

async def clio_1(update: Update, context: CallbackContext):
    url = "https://www.curs.md/ro/office/cliof1"

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
###################################################################################################

async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(update.message.text)

def main() -> None:
    application = Application.builder().token("6352522804:AAH1ucmVNQOWpPHP1Qce6FTexOCrOOKNQ1M").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(CommandHandler("haha", haha))
    application.add_handler(CommandHandler("bnm", bnm_rate))
    application.add_handler(CommandHandler("clio", clio))
    application.add_handler(CommandHandler("cliocsv", clio_csv))
    application.add_handler(CommandHandler("clio1", clio_1))

    application.run_polling()

if __name__ == '__main__':
    main()




