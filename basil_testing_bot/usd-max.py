from aiohttp import ClientSession
from bs4 import BeautifulSoup
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from fetch_data import *
from datetime import datetime



async def get_usd_max_rate() -> str:
    url = "https://www.curs.md/ro/curs_valutar_banci"
    async with ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            data = []  # Используем этот список для сбора данных

            rows = soup.find_all('tr')
            for row in rows:
                bank_data = row.find('td', class_='bank_name')
                if bank_data:
                    bank_name = bank_data.a.text.strip()
                    if "Banca Nationala" not in bank_name:
                        usd_values = row.find_all('td', class_='column-USD')
                        cump_usd = usd_values[0].text.strip().replace(",", ".")
                        vanz_usd = usd_values[1].text.strip().replace(",", ".")
                        # Преобразуем в float
                        cump_usd_float = float(cump_usd)
                        vanz_usd_float = float(vanz_usd)
                        data.append({
                            "bank_name": bank_name,
                            "cump_usd": f'{cump_usd_float:.2f}',
                            "vanz_usd": f'{vanz_usd_float:.2f}',
                            "cump_usd_float": cump_usd_float
                        })

            # Сортируем по cump_usd_float от максимального к минимальному
            sorted_data = sorted(data, key=lambda x: x['cump_usd_float'], reverse=True)

            # Формируем результат
            result = [f"<b>{item['bank_name']:35}</b>{item['cump_usd']:>5} / {item['vanz_usd']:5}" for item in sorted_data]
            
            return '\n'.join(result)


async def usd_max_rate(update: Update, context: CallbackContext) -> None:
    rate_message = await get_usd_max_rate()
    await update.message.reply_text(rate_message, parse_mode="HTML")