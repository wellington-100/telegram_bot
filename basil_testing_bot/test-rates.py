from aiohttp import ClientSession
from bs4 import BeautifulSoup
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from fetch_data import *
from datetime import datetime
import re


async def get_rate(currency: str, sort_key: str, reverse: bool = False) -> str:
    url = "https://www.curs.md/ro/curs_valutar_banci"
    column_class = f"column-{currency}"

    async with ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            date = soup.find('input', {'id': 'BanksCotDate'})['value']
            data = []
            ignore_words = ["Sucursala", "Filiala", "Centrală", "(Everest)", "(Trușeni)"]

            rows = soup.find_all('tr')
            for row in rows:
                bank_data = row.find('td', class_='bank_name')
                if bank_data:
                    bank_name = bank_data.a.text.strip()
                    for word in ignore_words:
                        bank_name = bank_name.replace(word, "") 
                    bank_name = bank_name.strip()  
                    if "Banca Nationala" not in bank_name:
                        values = row.find_all('td', class_=column_class)
                        cump = values[0].text.strip().replace(",", ".")
                        vanz = values[1].text.strip().replace(",", ".")

                        if not (re.match(r'^-?\d+(?:\.\d+)?$', cump) and re.match(r'^-?\d+(?:\.\d+)?$', vanz)):
                            continue 
                        
                        cump_float = float(cump)
                        vanz_float = float(vanz)
                        data.append({
                            "bank_name": bank_name,
                            "cump": f'{cump_float:.2f}',
                            "vanz": f'{vanz_float:.2f}',
                            sort_key: cump_float if sort_key == 'cump_float' else vanz_float
                        })

            sorted_data = sorted(data, key=lambda x: x[sort_key], reverse=reverse)
            result = [f"<pre><b>{item['bank_name']:20}</b> {item['cump']:>5}  {item['vanz']:5}</pre>" for item in sorted_data]
            result.insert(0, f"<b>RATE DE SCHIMB: {currency}/MDL</b> {date}\n")
            result.insert(1,f"<code>{'Banca/CSV':<19}{'Cump.':>7}{'Vanz.':>7}</code>\n")

            return '\n'.join(result)


async def custom_rate(update: Update, context: CallbackContext, currency: str, sort_key: str, reverse: bool = False) -> None:
    rate_message = await get_rate(currency, sort_key, reverse)
    await update.message.reply_text(rate_message, parse_mode="HTML")

