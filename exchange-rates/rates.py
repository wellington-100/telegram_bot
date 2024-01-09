from aiohttp import ClientSession
from bs4 import BeautifulSoup
from telegram import Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import re
import aioredis
import asyncio
from datetime import datetime, time
import json
from currency_info import currency_flags, currency_codes
from urls import urls
from typing import Tuple




async def get_rates(currency: str, show_all=False) -> Tuple[str, int]:
    url = f"https://www.curs.md/ro/valuta/{currency}"
    
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
    exclusions = ["SRL", "CSV", "Tighina", "Filiala", "Banca Nationala", "Sucursala", "Bancă", "Invest", "\""]
    replacements = {
        "BNM": "BNM / Curs oficial",
        # "Filiala 2": "2",
        # "Filiala 3": "3",
        # "Filiala 4": "4",
        # "Filiala 7": "7",
        # "Filiala 9": "9",
        # "Sucursala 1": "1",
        # "Sucursala 2": "2",
        # "Sucursala 3": "3",
        # "Sucursala 4": "4",
        # "Sucursala 5": "5",

    }
    data = []   
    for row in rows:
        bank_name_cell = row.find('td', class_='bank_name')
        if bank_name_cell is None:
            continue

        # Удаление тегов <sup> и их содержимого
        for sup_tag in bank_name_cell.find_all('sup'):
            sup_tag.decompose()

        bank_name = bank_name_cell.get_text(strip=True)
        # Применение замен
        for old, new in replacements.items():
            bank_name = bank_name.replace(old, new)

        # Удаление исключений
        for exclusion in exclusions:
            bank_name = bank_name.replace(exclusion, "")
        
        bank_name = re.sub(r'\s+', ' ', bank_name).strip()
        bank_name = re.sub(r'\(.*?\)', '', bank_name).strip()
        # if "Banca Nationala" in bank_name:
        #     continue

        cols = row.find_all('td', class_=f'column-{currency}')

        if cols:
            cump = cols[0].text.strip().replace(",", ".")
            vanz = cols[1].text.strip().replace(",", ".")

            # Преобразование в float и форматирование
            try:
                cump_float = float(cump)
                vanz_float = float(vanz)
                data.append((bank_name, cump_float, vanz_float))  # Добавление данных в список data
            except ValueError:
                continue
    data.sort(key=lambda x: x[1], reverse=True)

# Формирование строки результатов после сортировки
    original_data_count = len(data)

    # Сокращаем список данных до первых 15 записей, если show_all = False
    if not show_all:
        data = data[:15]

    # Формирование строки результатов после сортировки
    results = []
    for item in data:
        results.append(f"<pre><b>{item[0]:20}</b> {item[1]:.2f}  {item[2]:.2f}</pre>")

    if not results:
        return f"Нет данных по валюте {currency}.", original_data_count
   
    selected_currency_flag = currency_flags.get(currency, "")
    results_str = '\n'.join(results)
    header = f"<b>RATE DE SCHIMB VALUTAR / {formatted_date or 'Lipsă dată'}\n{selected_currency_flag} {currency} / MDL {currency_flags['MDL']}</b>\n\n"
    return header + results_str, original_data_count


async def custom_rates(update: Update, context: CallbackContext) -> None:
    currency = update.message.text[1:].upper()
    if currency not in currency_codes:
        await update.message.reply_text("Неподдерживаемая валюта", parse_mode="HTML")
        return
    rates_message, data_count = await get_rates(currency)
    
    # Проверяем, нужно ли добавить кнопку "Показать больше"
    if data_count > 15:
        buttons = [[InlineKeyboardButton("... vizualizați mai multe", callback_data=f"all_rates_{currency}")]]
        reply_markup = InlineKeyboardMarkup(buttons)
    else:
        reply_markup = None

    await update.message.reply_text(rates_message, reply_markup=reply_markup, parse_mode="HTML")


async def handle_all_rates(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    # Получаем валюту из callback_data
    currency = query.data.split('_')[-1]
    rates_message, _ = await get_rates(currency, show_all=True)

    await query.message.edit_text(rates_message, parse_mode="HTML")





async def get_bnm_rate(show_all=False) -> Tuple[str, int]:
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

            data = []
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
                    data.append((flag, currency, rate, change_full))
            original_data_count = len(data)

    # Формирование итогового сообщения
    if not show_all:
        data = data[:5]

    # Формирование итогового сообщения
    message_lines = [f" <b>CURS OFICIAL BNM {currency_flags['MDL']} pentru {formatted_date}</b>\n"]
    for item in data:
        message_lines.append(f"{item[0]}<code> {item[1]:<7} {item[2]:10} {item[3]:>10}</code>")

    return "\n".join(message_lines), original_data_count


async def bnm_rate(update: Update, context: CallbackContext) -> None:
    rate_message, data_count = await get_bnm_rate()

    if data_count > 5:
        buttons = [[InlineKeyboardButton("... vizualizați mai multe", callback_data="all_bnm_rates")]]
        reply_markup = InlineKeyboardMarkup(buttons)
    else:
        reply_markup = None

    await update.message.reply_text(rate_message, reply_markup=reply_markup, parse_mode="HTML")


async def handle_all_bnm_rates(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    rates_message, _  = await get_bnm_rate(show_all=True)
    await query.message.edit_text(rates_message, parse_mode="HTML")


