from telegram import ReplyKeyboardMarkup

MENU, MENU_ITEMS, TASK, DATE, HOUR, MINUTE, RESULT, CHOICE = range(8)

GO = "Вперед"
(
    CREATE,
    READ,
    UPDATE,
    DELETE,
    DONE,
) = "📝 Добавить задачу 📝, 🖥 Показать задачи 🖥, ⚙️ Изменить задачу ⚙️, 🔥 Удалить задачу 🔥, ✅ Отметить выполненной ✅".split(
    ", "
)
TODO_TEXT, TODO_DATE, TODO_TIME = "Текст задачи", "Дата задачи", "Время задачи"
menu = [[READ], [CREATE, DONE], [UPDATE, DELETE]]
RU_STEP = dict(y="год", m="месяц", d="день")
MONTHS = {
    1: "января",
    2: "февраля",
    3: "марта",
    4: "апреля",
    5: "мая",
    6: "июня",
    7: "июля",
    8: "августа",
    9: "сентября",
    10: "октября",
    11: "ноября",
    12: "декабря",
}
keyboard = ReplyKeyboardMarkup(
    menu,
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Да прибудет с тобой выбор!",
)
