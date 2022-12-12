from constants import GO, MENU, MENU_ITEMS, keyboard
from database_module import init
from interrupt import delete_message
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext


def start(update: Update, context: CallbackContext):
    keyboard = [[GO]]
    markup_key = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    name = update.effective_user.full_name
    abilities = f'''
    Добрый день, мастер {name}! Меня зовут R2-D2. Я помогу тебе планировать дела.
    Вот что я могу:
    - Добавить задачу
    - Изменить задачу
    - Удалить задачу
    - Отметить выполненной
    - Показать все задачи
    '''
    context.bot.send_sticker(
        update.effective_chat.id, 'CAACAgUAAxkBAAIMm2NxBzaiPxaOSiO-cKjg-hB3wqKeAAKFCAACxlHGFZDFxHAlU0V5KwQ')
    context.bot.send_message(update.effective_chat.id, abilities)
    update.message.reply_text(
        f'Для продолжения нажми на "{GO}"', reply_markup=markup_key)
    init(update, context)
    return MENU


def main_menu(update: Update, context: CallbackContext):
    name = update.effective_user.full_name
    delete_message(update, context, end=5)
    update.message.reply_sticker(
        'CAACAgUAAxkBAAIMoWNxPEpPFIYxDk36E0VB8gevaMxnAAJ4CAACxlHGFb7XhQmC5BIEKwQ')
    update.message.reply_text(
        f'Выберите, что хотите сделать, мастер {name}?', reply_markup=keyboard)
    return MENU_ITEMS



