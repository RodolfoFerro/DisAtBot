from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from ._credentials.py import *

updater = Updater(token=telegram_token)
dispatcher = updater.dispatcher


def start(bot, update):
    # Intro message
    hi = "Hello, I'm DisAtBot. / Hola, soy DisAtBot. \n\n"
    init = "To start, please select a language. / \
Para iniciar, por favor selecciona un idioma."
    bot.send_message(chat_id=update.message.chat_id, text=hi + init)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
#
#
# def chem_data(bot, update):
#     # Print user info:
#     first = update.message.from_user.first_name
#     last = update.message.from_user.last_name
#     print("Request from: {} {}".format(first, last))
#
#     # Requested info:
#     molecule = update.message.text
#     mol_msg = "Molecule requested: {} \nSearching molecule...".format(molecule)
#     bot.send_message(chat_id=update.message.chat_id, text=mol_msg)
#
#     # Search requested molecule:
#     img, smiles = scraper(molecule)
#     if smiles is None:
#         error = "Molecule not found. Maybe the name is misswritten... (?)"
#         bot.send_message(chat_id=update.message.chat_id, text=error)
#     else:
#         smiles_msg = "SMILES: {}".format(smiles)
#         bot.send_message(chat_id=update.message.chat_id, text=smiles_msg)
#         bot.send_photo(chat_id=update.message.chat_id,
#                        photo=open('molecule.png', 'rb'))
#
#
# drawing_handler = MessageHandler(Filters.text, chem_data)
# dispatcher.add_handler(drawing_handler)
