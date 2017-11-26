# ===============================================================
# Author: Rodolfo Ferro Pérez
# Email: ferro@cimat.mx
# Twitter: @FerroRodolfo
#
# ABOUT COPYING OR USING PARTIAL INFORMATION:
# This script was originally created by Rodolfo Ferro. Any
# explicit usage of this script or its contents is granted
# according to the license provided and its conditions.
# ===============================================================

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import ConversationHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from lang_dict import *
import logging

# You might need to add your tokens to this file...
from credentials import *


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

# Global vars:
LANG = "ES"
INIT, MENU, SET, REPORT, MAP, FAQ, ABOUT, BACK = range(8)


def start(bot, update):
    """
    Start function. Displayed whenever the /start command is called.
    This function sets the language of the bot.
    """
    # Create buttons to slect language:
    keyboard = [[InlineKeyboardButton("ES", callback_data='ES'),
                 InlineKeyboardButton("EN", callback_data='EN')]]

    # Create initial message:
    message = "Hey, I'm DisAtBot! / ¡Hey, soy DisAtBot! \n\n \
Please select a language to start. / Por favor selecciona un idioma \
para comenzar."

    reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text(message, reply_markup=reply_markup)

    return INIT


def set_lang(bot, update):
    """
    First handler with received data to set language globally.
    """
    # Set language:
    query = update.callback_query
    global LANG
    LANG = query.data

    logger.info(lang_selected[LANG])
    bot.send_message(text=lang_selected[LANG],
                     chat_id=query.message.chat_id,
                     message_id=query.message.message_id)

    return MENU


def menu(bot, update):
    """
    Main menu function.
    This will display the options from the main menu.
    """
    # Create buttons to slect language:
    keyboard = [[InlineKeyboardButton(send_report[LANG], callback_data=REPORT),
                 InlineKeyboardButton(view_map[LANG], callback_data=MAP)],
                [InlineKeyboardButton(view_faq[LANG], callback_data=FAQ),
                 InlineKeyboardButton(view_about[LANG], callback_data=ABOUT)]]

    reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text(main_menu[LANG], reply_markup=reply_markup)

    return SET


def set_action(bot, update):
    """
    Set option selected from menu.
    """
    query = update.callback_query
    option = query.data

    logger.info(selection[LANG].format(option))
    return option


def help(bot, update):
    """
    Help function.
    This displays a set of commands available for the bot.
    """
    update.message.reply_text("Use /start to restart DisAtBot.")


def cancel(bot, update):
    """
    User cancelation function.
    Cancel conersation by user.
    """
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(goodbye[LANG],
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """
    Main function.
    This controls all conversation and interactions with bot handlers.
    """
    # Create the Updater and pass it bot's token:
    updater = Updater(telegram_token)

    # =============================
    # Get the dispatcher to register handlers:
    dp = updater.dispatcher

    # Add conversation handler with the states
    # MENU, REPORT, MAP, FAQ and ABOUT:
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            INIT: [CallbackQueryHandler(set_lang)],

            MENU: [CommandHandler('menu', menu)],

            SET: [CallbackQueryHandler(set_action)],

            # REPORT: [MessageHandler(Filters.photo, photo),
            #         CommandHandler('skip', skip_photo)],
            # MAP: [MessageHandler(Filters.location, location),
            #            CommandHandler('skip', skip_location)],
            # FAQ: [MessageHandler(Filters.text, bio)],
            # ABOUT: [MessageHandler(Filters.text, bio)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # =============================
    # # Create handlers:
    # updater.dispatcher.add_handler(CommandHandler('start', start))
    # updater.dispatcher.add_handler(CallbackQueryHandler(set_lang))
    # updater.dispatcher.add_handler(CommandHandler('menu', menu))
    # updater.dispatcher.add_handler(CallbackQueryHandler(set_action))
    # updater.dispatcher.add_handler(CommandHandler('help', help))
    # updater.dispatcher.add_error_handler(error)

    # Start DisAtBot:
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process
    # receives SIGINT, SIGTERM or SIGABRT:
    updater.idle()


if __name__ == '__main__':
    main()
