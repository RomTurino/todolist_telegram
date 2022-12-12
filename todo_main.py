from config import TOKEN
from telegram.ext import Updater
from handlers import contact_handler


updater = Updater(TOKEN)
dispatcher = updater.dispatcher


dispatcher.add_handler(contact_handler)
print("started:", updater.bot.first_name)
updater.start_polling()
updater.idle()
