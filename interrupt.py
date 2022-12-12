from constants import keyboard
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, ConversationHandler


def cancel(update: Update, context: CallbackContext):
    update.message.reply_sticker(
        'CAACAgUAAxkBAAIMpGNxPMjnrNdRVTIaTHfKG9V4Vl6mAAKCCAACxlHGFeu8y1It091IKwQ')
    update.message.reply_text('Спасибо за использование списка задач, мастер!',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def endpoint(update: Update, context: CallbackContext):
    update.message.reply_sticker(
        'CAACAgQAAxkBAAIOzWN4rXlk0YnpSsLZ0FbyAAFeGEBv1AACpgMAAoIVwR1jsX9VcFk4yCsE')
    update.message.reply_text('Вы решили не добавлять новой задачи',
                              reply_markup=keyboard)
    return ConversationHandler.END

def wrong_message(update: Update, context: CallbackContext):
    update.message.reply_sticker(
        'CAACAgUAAxkBAAIOx2N4mLSkQWGFUqqzpaTTmfmqizeeAAKBCAACxlHGFZXfauYX-8AwKwQ')
    update.message.reply_text('Такой команды нет', reply_markup=keyboard)
    

def delete_message(update: Update, context: CallbackContext, start=0, end=5):
    for i in range(start,end):
        try:
            context.bot.delete_message(update.effective_chat.id, update.effective_message.message_id-i)
        except:
            continue