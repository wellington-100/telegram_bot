from aiohttp import ClientSession
from bs4 import BeautifulSoup
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from fetch_data import *
from rates import *
from datetime import datetime


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Я ваш простой бот.')

async def haha(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Что с тобой?')

async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(update.message.text)


#######################################################################################
async def universal_rate(update: Update, context: CallbackContext) -> None:
    currency = update.message.text[1:].upper() 
    await custom_rate(update, context, currency, 'cump_float', True)

async def universal_min_rate(update: Update, context: CallbackContext) -> None:
    command = update.message.text[1:]  
    currency = command[:-3]  
    await custom_rate(update, context, currency.upper(), 'vanz_float', False)

    
###################################### bnm  ############################################
async def get_bnm_rate() -> str:
    url = "https://www.curs.md/ro/curs_valutar_banci"
    async with ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            
            date_elem = soup.find('input', {'id': 'BoxCotDate'})
            if not date_elem:
                return "Ошибка при извлечении даты"
            date_value = date_elem.get('value')

            rows = soup.find_all('tr')
            rates = {}
            for row in rows:
                cells = row.find_all('td')
                if cells and len(cells) >= 3 and cells[1].get_text() in ["USD", "EUR", "RUB", "RON", "UAH", "GBP", "CHF", "TRY", "CAD"]:
                    currency = cells[1].get_text()
                    rate = cells[2].get_text().replace(" Lei", "")
                    
                    change_value = cells[3].get_text().split()[0] 

                    arrow_up = "▲"  # ↑
                    arrow_down = "▼"  # ↓
                    
                    if "-" in change_value:
                        change_direction = arrow_down
                    elif change_value == "0" or change_value == "0,0000":
                        change_direction = ""
                    else:
                        change_direction = arrow_up

                    change_full = f"{change_value} {change_direction}"
                    
                    rates[currency] = {"rate": rate, "change": change_full}
            if rates:
                message_lines = [f"<b>Cursul Oficial BNM pentru {date_value}</b>\n"]
                
                for key, data in rates.items():
                    message_lines.append(f"<code>{key:<10} {data['rate']:10} {data['change']:>10}</code>")
                return "\n".join(message_lines)

async def bnm_rate(update: Update, context: CallbackContext) -> None:
    rate_message = await get_bnm_rate()
    await update.message.reply_text(rate_message, parse_mode="HTML")


############################################### CLIO    ##########################################
async def clio (update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Alegeți Filiala:\n/cliocsv(Central),\n/clio1(Filiala 1),\n/clio2(Filiala 2),\n/clio3(Filiala 3),\n/clio4(Filiala 4)')
           
############################################### DEGHEST    ##########################################
async def deghest (update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Alegeți Filiala:\n/deghestcsv(Central),\n/deghest1(Filiala 1),\n/deghest2(Filiala 2)')
        
           
###################################################################################################


def main() -> None:
    application = Application.builder().token("6352522804:AAH1ucmVNQOWpPHP1Qce6FTexOCrOOKNQ1M").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("clio", clio))
    application.add_handler(CommandHandler("deghest", deghest))
    application.add_handler(CommandHandler("bnm", bnm_rate))

    for currency_code in ['usd', 'eur', 'rub', 'uah', 'ron', 'gbp', 'chf', 'try', 'cad', 'aed', 'aud', 'bgn', 'byn', 'cny', 'czk', 'dkk', 'hrk', 'huf', 'ils', 'jpy', 'nok', 'pln', 'sek']:
        application.add_handler(CommandHandler(f"{currency_code}", universal_rate))
        application.add_handler(CommandHandler(f"{currency_code}min", universal_min_rate))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.COMMAND, command_handler)) 
    application.run_polling()

if __name__ == '__main__':
    main()




