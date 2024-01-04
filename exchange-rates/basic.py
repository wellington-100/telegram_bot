from aiohttp import ClientSession
from bs4 import BeautifulSoup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler, ContextTypes
from fetch_data import *
from rates import *
from datetime import datetime
from config import TELEGRAM_TOKEN
from currency_info import *


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("Функция start вызвана")  # Логирование вызова функции start
    keyboard = [
        ['Bănci', 'Case de schimb valutar'],
        ['Valute', 'Alerte']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text('Alegeți o opțiune din meniu:', reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = str(update.message.text).strip()  # Добавляем .strip() для удаления лишних пробелов
    if text == 'Bănci':
        reply_text = '<b>Lista băncilor comerciale:</b>\n\n' + '\n'.join(banks)
        await update.message.reply_text(reply_text, parse_mode='HTML')
    elif text == 'Case de schimb valutar':
        reply_text = '<b>Lista caselor de schimb valutar:</b>\n\n' + '\n'.join(exchanges)
        await update.message.reply_text(reply_text, parse_mode='HTML')
    elif text == 'Valute':
        reply_text = '<b>Lista valutelor disponibile:</b>\n\n' + '\n'.join(currency_commands)
        await update.message.reply_text(reply_text, parse_mode='HTML')
    elif text == 'Alerte':
        reply_text = '<b>Valute disponibile:</b>\n\n' + '\n'.join(currency_commands)
        await update.message.reply_text(reply_text, parse_mode='HTML')
    else:
        await update.message.reply_text(f'Ați ales: {text}')

#--------------------------------------------- CLIO    ---------------------------------------------
async def clio (update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Alegeți Filiala:\n/cliocsv(Central),\n/clio1(Filiala 1),\n/clio2(Filiala 2),\n/clio3(Filiala 3),\n/clio4(Filiala 4)')  
#--------------------------------------------- DEGHEST    -------------------------------------------
async def deghest (update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Alegeți Filiala:\n/deghestcsv(Central),\n/deghest1(Filiala 1),\n/deghest2(Filiala 2)')
#--------------------------------------------- ARMETIS    ------------------------------------------
async def armetis (update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Alegeți Filiala:\n/armetisgrup(Central),\n/armetis1(Sucursala 1),\n/armetis2(Sucursala 2),\n/armetis3(Sucursala 3),\n/armetis4(Sucursala 4),\n/armetis5(Sucursala 5)')      
#---------------------------------------------------------------------------------------------------

def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(start_handler)
    application.add_handler(message_handler)
    

    application.add_handler(CommandHandler("clio", clio))
    application.add_handler(CommandHandler("deghest", deghest))
    application.add_handler(CommandHandler("bnm", bnm_rate))
    application.add_handler(CommandHandler("armetis", armetis))

    for currency_code in currency_codes:
        application.add_handler(CommandHandler(f"{currency_code}", custom_rates))
 
    application.add_handler(MessageHandler(filters.COMMAND, command_handler)) 

    application.run_polling()

if __name__ == '__main__':
    main()



#######################################################################################
# async def universal_rate(update: Update, context: CallbackContext) -> None:
#     currency = update.message.text[1:].upper() 
#     await custom_exotic_rates(update, context, currency, 'cump_float', True)

# async def universal_min_rate(update: Update, context: CallbackContext) -> None:
#     command = update.message.text[1:]  
#     currency = command[:-3]  
#     await custom_exotic_rates(update, context, currency.upper(), 'vanz_float', False)



# async def clio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     keyboard = [
#         [InlineKeyboardButton("Clio Filiala 1", callback_data='/clio1 (Accesați comanda...)'),
#          InlineKeyboardButton("Clio Filiala 2", callback_data='/clio2')],
#         [InlineKeyboardButton("Clio Filiala 3", callback_data='/clio3'),
#          InlineKeyboardButton("Clio Filiala 4", callback_data='/clio4')],
#         [InlineKeyboardButton("Clio Centrala", callback_data='/cliocsv')]
#     ]

#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.message.reply_text('Alegeți Cetrala sau una din filiale:', reply_markup=reply_markup)

# async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     query = update.callback_query
#     await query.answer()

#     command = query.data

#     # Отправляем команду как текстовое сообщение
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=command)


# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     keyboard = [
#         [InlineKeyboardButton("Опция 1", callback_data='1'),
#          InlineKeyboardButton("Опция 2", callback_data='2')],
#         [InlineKeyboardButton("Опция 3", callback_data='3')]
#     ]

#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.message.reply_text('Пожалуйста, выберите опцию:', reply_markup=reply_markup)

# async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     query = update.callback_query
#     await query.answer()
#     await query.edit_message_text(text=f"Выбрана опция: {query.data}")