from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from credentials import *
from lang_dict import *
import logging


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

# Local vars:
LANG = "ES"


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

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(message, reply_markup=reply_markup)

    return


def set_lang(bot, update):
    """
    First handler with received data to set language globally.
    """
    # Set language:
    query = update.callback_query
    global LANG
    LANG = query.data

    bot.edit_message_text(text=lang_selected[LANG],
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

    return


def help(bot, update):
    """
    Help function.
    This displays a set of commands available for the bot.
    """
    update.message.reply_text("Use /start to restart DisAtBot.")


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

    # Create handlers:
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(set_lang))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_error_handler(error)

    # Start DisAtBot:
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process
    # receives SIGINT, SIGTERM or SIGABRT:
    updater.idle()


if __name__ == '__main__':
    main()
