from aiohttp import ClientSession
from bs4 import BeautifulSoup
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from fetch_data import *
from datetime import datetime


async def get_rate() -> str:
    url = "https://www.curs.md/ro/curs_valutar_banci"
    async with ClientSession() as session:
        async with session.get(url) as response:

            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            result = []

            result.append("<code>Banca/CSV___USD___cump.___vanz.</code>")
            rows = soup.find_all('tr')
            for row in rows:
                bank_data = row.find('td', class_='bank_name')
                if bank_data:
                    bank_name = bank_data.a.text.strip()
                    if "Banca Nationala" not in bank_name:
                        usd_values = row.find_all('td', class_='column-USD')
                        cump_usd = usd_values[0].text.strip()
                        vanz_usd = usd_values[1].text.strip()
                        cump_usd = f'{float(cump_usd.replace(",", ".")):.2f}'
                        vanz_usd = f'{float(vanz_usd.replace(",", ".")):.2f}'
                        result.append(f"<code>{bank_name:15} {cump_usd:10} {vanz_usd:10}</code>")

            return '\n'.join(result)


async def bank_rate(update: Update, context: CallbackContext) -> None:
    rate_message = await get_rate()
    await update.message.reply_text(rate_message, parse_mode="HTML")
