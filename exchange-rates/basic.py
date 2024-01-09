from aiohttp import ClientSession
from bs4 import BeautifulSoup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler, ContextTypes
from fetch_data import *
from rates import *
from datetime import datetime
from config import TELEGRAM_TOKEN
from currency_info import *
from user import *


def user_exists(user_id):
    """ Проверка, существует ли пользователь в базе данных """
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT EXISTS(SELECT 1 FROM users WHERE user_id = %s);", (user_id,))
    exists = cur.fetchone()[0]
    cur.close()
    conn.close()
    return exists

def add_user_if_not_exists(user_id, username=None):
    """ Добавление пользователя, если он не существует """
    if not user_exists(user_id):
        add_user(user_id, username)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("Функция start вызвана")  # Логирование вызова функции start

    user_id = update.effective_user.id
    username = update.effective_user.username

    # Добавить пользователя в базу данных, если его там нет
    add_user_if_not_exists(user_id, username)

    keyboard = [
        ['Bănci', 'Case de schimb valutar'],
        ['Valute', 'Alerte']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text('Alegeți o opțiune din meniu:', reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = str(update.message.text).strip()  # Удаление лишних пробелов

    # Основное меню
    main_menu_keyboard = [
        ['Bănci', 'Case de schimb valutar'],
        ['Valute', 'Alerte']
    ]
    main_menu_reply_markup = ReplyKeyboardMarkup(main_menu_keyboard, one_time_keyboard=True, resize_keyboard=True)

    # Меню для 'Alerte'
    alerte_menu_keyboard = [
        ['Adaugă alertă', 'Alertele mele'],
        ['Înapoi']
    ]
    alerte_menu_reply_markup = ReplyKeyboardMarkup(alerte_menu_keyboard, one_time_keyboard=True, resize_keyboard=True)

    if text == 'Bănci':
        reply_text = '<b>Lista băncilor comerciale:</b>\n\n' + '\n'.join(banks)
        await update.message.reply_text(reply_text, parse_mode='HTML')
    elif text == 'Case de schimb valutar':
        reply_text = '<b>Lista caselor de schimb valutar:</b>\n\n' + '\n'.join(exchanges)
        await show_exchanges(update, context)
    elif text == 'Valute':
        # Отображаем только первые 20 записей
        first_20_commands = '\n'.join(currency_commands[:20])
        reply_text = f'<b>Lista valutelor disponibile:</b>\n\n{first_20_commands}'

        # Добавляем кнопку "Показать больше", если в списке больше 20 элементов
        if len(currency_commands) > 20:
            buttons = [[InlineKeyboardButton("... vizualizați mai multe", callback_data="all_currency_commands")]]
            reply_markup = InlineKeyboardMarkup(buttons)
        else:
            reply_markup = None

        await update.message.reply_text(reply_text, reply_markup=reply_markup, parse_mode='HTML')
    elif text == 'Alerte':
        # Показать меню 'Alerte'
        await update.message.reply_text('Alegeți o opțiune:', reply_markup=alerte_menu_reply_markup)
    elif text == 'Înapoi':
        # Вернуться к главному меню
        await update.message.reply_text('Alegeți o opțiune din meniu:', reply_markup=main_menu_reply_markup)
    else:
        await update.message.reply_text(f'Ați ales: {text}')

#---------------------------    MORE    -----------------------------------------------------------------
async def show_exchanges(update: Update, context: ContextTypes.DEFAULT_TYPE, start_index=0, all_exchanges=False):
    # Если запрашивается показ всего списка
    if all_exchanges:
        exchanges_to_show = exchanges
        reply_markup = None  # Не нужна кнопка "Показать больше"
    else:
        # Пагинация для первых 15 элементов
        page_size = 20
        end_index = start_index + page_size
        exchanges_to_show = exchanges[start_index:end_index]

        buttons = []
        # Добавляем кнопку "Arată toate...", если в списке ещё есть элементы
        if end_index < len(exchanges):
            buttons.append([InlineKeyboardButton("... vizualizați mai multe", callback_data="all_exchanges")])
        reply_markup = InlineKeyboardMarkup(buttons) if buttons else None

    reply_text = '\n'.join(exchanges_to_show)
    if update.callback_query:
        await update.callback_query.message.edit_text(reply_text, reply_markup=reply_markup, parse_mode='HTML')
    else:
        await update.message.reply_text(reply_text, reply_markup=reply_markup, parse_mode='HTML')

# Обработчик для показа всего списка
async def handle_all_exchanges(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_exchanges(update, context, all_exchanges=True)
#-----------------------------------------------------------------------------------------------------------------
async def handle_all_currency_commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    full_list = '\n'.join(currency_commands)
    reply_text = f'<b>Lista valutelor disponibile:</b>\n\n{full_list}'
    await query.message.edit_text(reply_text, parse_mode='HTML')

#-----------------------------------------------------------------------------------------------------------------




def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(CallbackQueryHandler(handle_all_currency_commands, pattern='^all_currency_commands$'))
    application.add_handler(CommandHandler("bnm", bnm_rate))
    application.add_handler(CallbackQueryHandler(handle_all_bnm_rates, pattern='^all_bnm_rates$'))
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(start_handler)
    application.add_handler(message_handler)


    application.add_handler(CallbackQueryHandler(handle_all_exchanges, pattern='^all_exchanges$'))

    


    for currency_code in currency_codes:
        application.add_handler(CommandHandler(f"{currency_code}", custom_rates))

    application.add_handler(CallbackQueryHandler(handle_all_rates, pattern='^all_rates_'))


 
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



# async def alerte(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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


# #--------------------------------------------- CLIO    ---------------------------------------------
# async def clio (update: Update, context: CallbackContext) -> None:
#     await update.message.reply_text('Alegeți Filiala:\n/cliocsv (Central),\n/clio1 (Filiala 1),\n/clio2 (Filiala 2),\n/clio3 (Filiala 3),\n/clio4(Filiala 4)')  
# #--------------------------------------------- DEGHEST    -------------------------------------------
# async def deghest (update: Update, context: CallbackContext) -> None:
#     await update.message.reply_text('Alegeți Filiala:\n/deghestcsv (Central),\n/deghest1 (Filiala 1),\n/deghest2 (Filiala 2)')
# #--------------------------------------------- ARMETIS    ------------------------------------------
# async def armetis (update: Update, context: CallbackContext) -> None:
#     await update.message.reply_text('Alegeți Filiala:\n/armetisgrup (Central),\n/armetis1 (Sucursala 1),\n/armetis2 (Sucursala 2),\n/armetis3(Sucursala 3),\n/armetis4(Sucursala 4),\n/armetis5(Sucursala 5)') 
# #--------------------------------------------- EXCLUSIV   ------------------------------------------
# async def exclusiv (update: Update, context: CallbackContext) -> None:
#     await update.message.reply_text('Alegeți Filiala:\n/exclusivcsv (Central),\n/exclusiv1 (Filiala 1),\n/exclusiv2 (Filiala 2)')      
# #--------------------------------------------- NELCAT  ------------------------------------------
# async def nelcat (update: Update, context: CallbackContext) -> None:
#     await update.message.reply_text('Alegeți Filiala:\n/nelcat1 (NELCAT CAPITAL),\n/nelcat2 (Filiala Kiev)')    
#   
    # application.add_handler(CommandHandler("clio", clio))
    # application.add_handler(CommandHandler("deghest", deghest))
    # application.add_handler(CommandHandler("armetis", armetis))
    # application.add_handler(CommandHandler("exclusiv", exclusiv))
    # application.add_handler(CommandHandler("nelcat", nelcat))
# #---------------------------------------------------------------------------------------------------