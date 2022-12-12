from constants import *
from database_module import read_tasks
from interrupt import cancel, endpoint, wrong_message
from start_menu import main_menu, start
from task_create import (add_task, handle_date, handle_hour, handle_minute,
                         handle_task_text, save_result)
from task_delete import delete_task, do_deletion
from task_update import (update_task, 
                         choose_action,
                         choose_direction,
                         save_update_result)
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler)
from telegram_bot_calendar import DetailedTelegramCalendar



add_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex(f"^{CREATE}$"), add_task)],
    states={
        # CallbackQueryHandler(handle_task_text)
        TASK: [MessageHandler(Filters.text & ~Filters.command, handle_task_text)],
        DATE: [CallbackQueryHandler(handle_date, DetailedTelegramCalendar.func)],
        HOUR: [CallbackQueryHandler(handle_hour)],
        MINUTE: [CallbackQueryHandler(handle_minute)],
        RESULT: [CallbackQueryHandler(save_result)],
    },
    fallbacks=[CommandHandler("no", endpoint)],
)

update_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex(f"^{UPDATE}$"), update_task)],
    states={
        # CallbackQueryHandler(handle_task_text)
        TASK: [MessageHandler(Filters.text & ~Filters.command, choose_action)],
        CHOICE: [MessageHandler(Filters.text & ~Filters.command, choose_direction)],
        RESULT: [CallbackQueryHandler(save_update_result)]
    },
    fallbacks=[CommandHandler("no", endpoint)],
)

delete_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex(f"^{DELETE}$"), delete_task)],
    states={
        TASK: [MessageHandler(Filters.text & ~Filters.command, do_deletion)]
    },
    fallbacks=[CommandHandler("no", endpoint)],
)

done_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex(f"^{DONE}$"), delete_task)],
    states={
        TASK: [MessageHandler(Filters.text & ~Filters.command, do_deletion)]
    },
    fallbacks=[CommandHandler("no", endpoint)],
)


contact_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        MENU: [MessageHandler(Filters.text, main_menu)],
        MENU_ITEMS: [
            MessageHandler(Filters.regex(f"^{READ}$"), read_tasks),
            add_handler,
            update_handler,
            delete_handler,
            done_handler,
            MessageHandler(Filters.text, wrong_message),
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
