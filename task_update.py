import csv
from constants import MONTHS, TASK, TODO_DATE, TODO_TEXT,  CHOICE, RESULT
from database_module import get_all_tasks, read_tasks, rewrite_database
from interrupt import delete_message
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, ConversationHandler
from task_create import DetailedTelegramCalendar, date, RU_STEP
from start_menu import main_menu


def update_task(update: Update, context: CallbackContext):
    name = update.effective_user.full_name
    delete_message(update, context, end=10)
    read_tasks(update, context)
    update.message.reply_sticker(
        "CAACAgIAAxkBAAIRpmOPX1FNe6vopID71Ya7lDtYzJWsAAJtIAACiLDJS5sPYj-39D6pKwQ"
    )
    update.message.reply_text(f"Какое дело изменить, мастер {name}?")
    return TASK


def choose_action(update: Update, context: CallbackContext):
    number = update.message.text
    if not number.isdigit():
        update.message.reply_text("Вы ввели не число")
        return
    number = int(number) - 1
    filename = context.user_data["file"]
    context.user_data["number"] = number
    task = get_all_tasks(filename)[number]
    keyboard = [[TODO_TEXT, TODO_DATE]]
    markup = ReplyKeyboardMarkup(keyboard)
    todo_text, date, time = task
    year, month, day = str(date).split("-")
    update.message.reply_text(
        f"""
                                      To Do №{number+1}:
                                      {todo_text}
                                      Дедлайн: {day} {MONTHS[int(month)]} {year}
                                      {time}
                                      """
    )
    update.message.reply_text("Что хочешь поменять?", reply_markup=markup)
    return CHOICE


def choose_direction(update: Update, context: CallbackContext):
    answer = update.message.text
    name = update.effective_user.first_name
    if answer == TODO_TEXT:
        update.message.reply_text(f"Что за дело, мастер {name}?",
                                  reply_markup=ReplyKeyboardRemove())
        context.user_data['content'] = TODO_TEXT
        return RESULT
    elif answer == TODO_DATE:
        calendar, step = DetailedTelegramCalendar(
            locale="ru", min_date=date.today()).build()
        context.bot.send_message(
            update.effective_chat.id, f"Выбери {RU_STEP[step]}", reply_markup=calendar
        )
        context.user_data['content'] = TODO_DATE
        return RESULT


def save_update_result(update: Update, context: CallbackContext):
    content = context.user_data['content']
    filename = context.user_data["file"]
    number = context.user_data["number"]
    if content == TODO_TEXT:
        message = update.message.text
        update.message.reply_text(f'Текст дела сохранен на "{message}"')
        tasks = get_all_tasks(filename)
        tasks[number][0] = message
    elif content == TODO_DATE:
        result, key, step = DetailedTelegramCalendar(
            locale="ru", min_date=date.today()
        ).process(update.callback_query.data)
        delete_message(update, context, end=2)
        if not result and key:
            context.bot.send_message(
                update.effective_chat.id, f"Выбери {RU_STEP[step]}", reply_markup=key
            )
            return
        tasks = get_all_tasks(filename)
        tasks[number][1] = result
        year, month, day = str(result).split("-")

        context.bot.send_message(
            update.effective_chat.id, f"Ты выбрал {day} {MONTHS[int(month)]} {year}"
        )
    rewrite_database(filename, tasks)
    
    main_menu(update, context)
    return ConversationHandler.END
