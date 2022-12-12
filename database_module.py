import csv
import os
from typing import List

from constants import MONTHS, keyboard
from interrupt import delete_message
from telegram import Update
from telegram.ext import CallbackContext


def init(update: Update, context: CallbackContext):
    username = update.effective_user.username
    filename = f'database/{username}.csv'
    context.user_data['file'] = filename
    if not os.path.exists('database'):
        os.mkdir('database')
    if not os.path.exists(filename):
        open(filename, 'w')


def get_all_tasks(filename:str):
    with open(filename, encoding='utf-8') as file:
        tasks = list(csv.reader(file, delimiter='|'))
        return tasks

def read_tasks(update: Update, context: CallbackContext):
    filename = context.user_data['file']
    tasks = get_all_tasks(filename)
    if not tasks:
        delete_message(update, context, end=1)
        update.message.reply_sticker(
            'CAACAgQAAxkBAAIOwWN4hsp_nUM89VfOdbo4kIAUkPzOAAIOCwACR5RRUYe5AqD0zYysKwQ')
        update.message.reply_text(
            'Никаких задач не обнаружено!', reply_markup=keyboard)
    else:
        for number,task in enumerate(tasks, start=1):
            todo_text, date, time = task
            year, month, day = str(date).split('-')
            update.message.reply_text(f'''
                                      To Do №{number}:
                                      {todo_text}
                                      Дедлайн: {day} {MONTHS[int(month)]} {year}
                                      {time}
                                      ''')
            

def rewrite_database(filename: str, tasks: List[str]):
    with open(filename, mode="w", encoding="utf-8") as file:
        file_writer = csv.writer(file, delimiter="|", lineterminator="\r")
        for task in tasks:
            file_writer.writerow(task)