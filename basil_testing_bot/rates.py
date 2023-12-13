from aiohttp import ClientSession
from bs4 import BeautifulSoup
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import re


async def get_rate(currency: str, sort_key: str = 'cump', reverse: bool = False) -> str:
    urls = [
        "https://www.curs.md/ro/office/francunic/csv",
        "https://www.curs.md/ro/office/franklin",
        "https://www.curs.md/ro/office/lozcoz",
        "https://www.curs.md/ro/office/oanta",
        "https://www.curs.md/ro/office/clioschimb"
    ]
    results = []

    for url in urls:
        async with ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                exchanger_name = soup.find('h1').text.strip()
                date = soup.find('input', {'id': 'BankCotDate'})['value']
                data = []
                table = soup.find('table', class_='table table-hover')
                rows = table.find_all('tr')[1:]

                for row in rows:
                    cols = row.find_all('td')
                    valuta = cols[0].text.strip()
                    cump = cols[3].text.strip().replace(",", ".")
                    vanz = cols[4].text.strip().replace(",", ".")

                    if valuta == currency:
                        cump_float = float(cump)
                        vanz_float = float(vanz)
                        data.append({
                            "valuta": valuta,
                            "cump": f'{cump_float:.2f}',
                            "vanz": f'{vanz_float:.2f}',
                            "cump_float": cump_float,
                            "vanz_float": vanz_float
                        })

                sorted_data = sorted(data, key=lambda x: x[sort_key], reverse=reverse)

                result = [f"<pre><b>{exchanger_name:20}</b> {item['cump']:>5}  {item['vanz']:5}</pre>" for item in sorted_data]
                results.extend(result)

    results.insert(0, f"<b>RATE DE SCHIMB: {currency}/MDL</b> {date}\n")
    results.insert(1, f"<code>{'Banca/CSV':<19}{'Cump.':>7}{'Vanz.':>7}</code>\n")

    return '\n'.join(results)


async def custom_rate(update: Update, context: CallbackContext, currency: str, sort_key: str, reverse: bool = False) -> None:
    rate_message = await get_rate(currency, sort_key, reverse)
    await update.message.reply_text(rate_message, parse_mode="HTML")


# Вставьте сюда код для работы бота с Telegram.
