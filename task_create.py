import csv
from datetime import date, time
from constants import DATE, HOUR, MINUTE, MONTHS, RESULT, RU_STEP, TASK
from interrupt import delete_message
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, ConversationHandler
from telegram_bot_calendar import DetailedTelegramCalendar


def add_task(update: Update, context: CallbackContext):
    name = update.effective_user.full_name
    delete_message(update, context, end=10)
    update.message.reply_sticker(
        "CAACAgQAAxkBAAIOymN4rJ6vunT_sJMWwfyPflWCus5lAAInCwAC61AhUavp5C2VaPGhKwQ"
    )
    update.message.reply_text(f"Что за дело, мастер {name}?")
    return TASK


def handle_task_text(update: Update, context: CallbackContext):
    message = update.message.text
    context.user_data["todo_text"] = message
    delete_message(update, context, end=4)
    calendar, step = DetailedTelegramCalendar(
        locale="ru", min_date=date.today()
    ).build()
    context.bot.send_message(
        update.effective_chat.id, f"Выбери {RU_STEP[step]}", reply_markup=calendar
    )
    return DATE


def handle_date(update: Update, context: CallbackContext):
    result, key, step = DetailedTelegramCalendar(
        locale="ru", min_date=date.today()
    ).process(update.callback_query.data)
    delete_message(update, context, end=2)
    if not result and key:
        context.bot.send_message(
            update.effective_chat.id, f"Выбери {RU_STEP[step]}", reply_markup=key
        )
        return
    context.user_data["date"] = result
    context.bot.send_message(
        update.effective_chat.id,
        "Дата выбрана",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Дальше", callback_data="Дальше")]]
        ),
    )
    return HOUR


def handle_hour(update: Update, context: CallbackContext):
    result = context.user_data["date"]
    year, month, day = str(result).split("-")

    context.bot.send_message(
        update.effective_chat.id, f"Ты выбрал {day} {MONTHS[int(month)]} {year}"
    )
    buttons = []
    plus = {0: 0, 1: 6, 2: 12, 3: 18}
    for j in range(4):
        buttons.append([])
        for i in range(6):
            buttons[j].append(
                InlineKeyboardButton(
                    f"{i+plus[j]}:00", callback_data=i + plus[j])
            )
    buttons = InlineKeyboardMarkup(buttons)

    context.bot.send_message(
        update.effective_chat.id,
        f"Выбери час к которому нужно дело завершить",
        reply_markup=buttons,
    )
    return MINUTE


def handle_minute(update: Update, context: CallbackContext):
    hour = update.callback_query.data
    context.user_data["hour"] = hour
    buttons = []
    plus = {0: 0, 1: 3, 2: 6, 3: 9}
    for j in range(4):
        buttons.append([])
        for i in range(3):
            char = ''
            if (i+plus[j]) * 5 <= 5:
                char = '0'
            buttons[j].append(
                InlineKeyboardButton(
                    f"{hour}:{char}{(i+plus[j]) * 5}", callback_data=(i + plus[j]) * 5
                )
            )
    buttons = InlineKeyboardMarkup(buttons)
    delete_message(update, context, start=1, end=2)
    context.bot.send_message(
        update.effective_chat.id,
        f"Выбери минуту к которой нужно дело завершить",
        reply_markup=buttons,
    )
    return RESULT


def save_result(update: Update, context: CallbackContext):
    minute = int(update.callback_query.data)
    info = context.user_data
    todo_text = info["todo_text"]
    date = info["date"]
    hour = int(info["hour"])
    filename = info["file"]
    delete_message(update, context, end=3)
    with open(filename, mode="a", encoding="utf-8") as file:
        file_writer = csv.writer(file, delimiter="|", lineterminator="\r")
        file_writer.writerow([todo_text, date, time(int(hour), int(minute))])
    context.bot.send_message(
        update.effective_chat.id,
        f"""
                                    To Do добавлено:
                                    {todo_text}
                                    Дедлайн: {date} {hour}:{minute} """
    )
    return ConversationHandler.END
