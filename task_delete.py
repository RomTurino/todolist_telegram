import csv
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from constants import TASK, DELETE, DONE
from database_module import read_tasks,get_all_tasks, rewrite_database
from interrupt import delete_message
from start_menu import main_menu


def delete_task(update: Update, context: CallbackContext):
    action = update.message.text
    name = update.effective_user.full_name
    delete_message(update, context, end=10)
    read_tasks(update, context)
    if action == DELETE:
        update.message.reply_sticker(
            "CAACAgIAAxkBAAISTWOW8RRxxry1Sr-I62K3MLkmNMOUAAJyIQACl7GgS15KZC-KWwtcKwQ"
        )
        update.message.reply_text(f"Какое дело удалить, мастер {name}?")
    elif action == DONE:
        update.message.reply_sticker(
            "CAACAgQAAxkBAAISU2OW-BR15QmW8y7oKVxNIPLtTnzNAAJUCgAC3biRURByIUwMpSpZKwQ"
        )
        update.message.reply_text(f"Какую задачу удалось выполнить, {name}?")
    context.user_data['action'] = action
    return TASK


def do_deletion(update: Update, context: CallbackContext):
    number = update.message.text
    if not number.isdigit():
        update.message.reply_text("Вы ввели не число")
        return
    number = int(number) - 1
    filename = context.user_data["file"]
    context.user_data["number"] = number
    tasks = get_all_tasks(filename)
    action = context.user_data['action']
    if action == DELETE:
        del tasks[number]
        update.message.reply_sticker(
            'CAACAgIAAxkBAAISUGOW9RxmRRn-taYx5T78oy_90YTuAAKmIAACqi_JS7Xn-BH1iuD0KwQ')
        update.message.reply_text("Задача удалена")
    elif action == DONE:
        new_base = filename[:-4]+'_done'+filename[-4:]
        with open(new_base, mode="a", encoding="utf-8") as file:
            file_writer = csv.writer(file, delimiter="|", lineterminator="\r")
            file_writer.writerow(tasks[number])
        del tasks[number]
        update.message.reply_sticker(
            'CAACAgIAAxkBAAISVmOW-mKlLr0ptuK4aK-XcxtbycfeAALGIwACBD6ZS_jfQrU3zwdbKwQ')
        update.message.reply_text("Задача отмечена выполненной")
    rewrite_database(filename, tasks)
    main_menu(update, context)
    return ConversationHandler.END