from aiohttp import ClientSession
from bs4 import BeautifulSoup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler, ContextTypes
from fetch_data import *
from rates import *
from datetime import datetime
from config import TELEGRAM_TOKEN


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Опция 1", callback_data='1'),
         InlineKeyboardButton("Опция 2", callback_data='2')],
        [InlineKeyboardButton("Опция 3", callback_data='3')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Пожалуйста, выберите опцию:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"Выбрана опция: {query.data}")
####################################################################################
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        ['Bănci', 'Schimburi Valutare'],
        ['Valute', 'Alerte']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text('Привет! Выберите опцию:', reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    await update.message.reply_text(f'Вы выбрали: {text}')







async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(update.message.text)



#######################################################################################
async def universal_rate(update: Update, context: CallbackContext) -> None:
    currency = update.message.text[1:].upper() 
    await custom_exotic_rates(update, context, currency, 'cump_float', True)

async def universal_min_rate(update: Update, context: CallbackContext) -> None:
    command = update.message.text[1:]  
    currency = command[:-3]  
    await custom_exotic_rates(update, context, currency.upper(), 'vanz_float', False)


############################################### CLIO    ##########################################
# async def clio (update: Update, context: CallbackContext) -> None:
#     await update.message.reply_text('Alegeți Filiala:\n/cliocsv(Central),\n/clio1(Filiala 1),\n/clio2(Filiala 2),\n/clio3(Filiala 3),\n/clio4(Filiala 4)')

async def clio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Clio Filiala 1", callback_data='/clio1 (Accesați comanda...)'),
         InlineKeyboardButton("Clio Filiala 2", callback_data='/clio2')],
        [InlineKeyboardButton("Clio Filiala 3", callback_data='/clio3'),
         InlineKeyboardButton("Clio Filiala 4", callback_data='/clio4')],
        [InlineKeyboardButton("Clio Centrala", callback_data='/cliocsv')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Alegeți Cetrala sau una din filiale:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    command = query.data

    # Отправляем команду как текстовое сообщение
    await context.bot.send_message(chat_id=update.effective_chat.id, text=command)


           
############################################### DEGHEST    ##########################################
async def deghest (update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Alegeți Filiala:\n/deghestcsv(Central),\n/deghest1(Filiala 1),\n/deghest2(Filiala 2)')

############################################### DEGHEST    ##########################################
async def armetis (update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Alegeți Filiala:\n/armetisgrup(Central),\n/armetis1(Sucursala 1),\n/armetis2(Sucursala 2),\n/armetis3(Sucursala 3),\n/armetis4(Sucursala 4),\n/armetis5(Sucursala 5)')
        
           
###################################################################################################


#... импорт библиотек и определения функций ...

def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Обычные обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.add_handler(CommandHandler("clio", clio))
    application.add_handler(CallbackQueryHandler(button))

    # application.add_handler(CommandHandler("clio", clio))
    application.add_handler(CommandHandler("deghest", deghest))
    application.add_handler(CommandHandler("bnm", bnm_rate))
    application.add_handler(CommandHandler("armetis", armetis))

    # Добавление обработчиков для кэшированных курсов валют
    for currency_code in ['usd', 'eur', 'rub', 'ron', 'uah', 'gbp', 'chf', 'try', 'cad']:
        application.add_handler(CommandHandler(f"{currency_code}", custom_basic_rates))
        application.add_handler(CommandHandler(f"{currency_code}min", cached_rate))

    for currency_code in ['eur', 'aed', 'aud', 'bgn', 'byn', 'cny', 'czk', 'dkk', 'hrk', 'huf', 'ils', 'jpy', 'nok', 'pln', 'sek']:
        application.add_handler(CommandHandler(f"{currency_code}", cached_rate))
        application.add_handler(CommandHandler(f"{currency_code}min", cached_rate))
        application.add_handler(CommandHandler("update", force_update))

    # Обработчик эхо-сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.COMMAND, command_handler)) 

    # Добавление команды в обработчик команд

    # Запуск планировщика для обновления кэша
    asyncio.get_event_loop().run_until_complete(create_redis_connection())

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()





