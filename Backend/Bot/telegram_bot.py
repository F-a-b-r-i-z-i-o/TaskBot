from telegram import Bot, Update, BotCommand
from telegram.ext import Updater, CommandHandler, CallbackContext
from decouple import config
from django.db import connection  
import logging
from TaskList.models import Task

# Set up logging for debugging and tracking
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


TELEGRAM_BOT_TOKEN = config("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = config("TELEGRAM_CHAT_ID")

# Initialize the bot and updater
bot = Bot(token=TELEGRAM_BOT_TOKEN)
updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Set the bot's command list
bot.set_my_commands([
    BotCommand("start", "Start the bot and show available commands"),
    BotCommand("add_task", "Add a new task: /add_task <title> <description> <YYYY-MM-DD>"),
    BotCommand("delete_task", "Delete a task by ID: /delete_task <id>"),
    BotCommand("tasks", "List all tasks"),
    BotCommand("complete_task", "Mark a task as completed: /complete_task <id>"),
])


def send_message(message):
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        '👋 Hello! You can manage your tasks with the following commands:\n'
        '1. Add a new task: /add_task <title> <description> <YYYY-MM-DD>\n'
        '2. Delete a task by ID: /delete_task <id>\n'
        '3. List all tasks: /tasks\n'
        '4. Mark a task as completed: /complete_task <id>'
    )


def add_task(update: Update, context: CallbackContext):
    from TaskList.models import Task
    try:
        # Extract task details from the command arguments
        title = context.args[0]
        description = ' '.join(context.args[1:-1])
        due_date = context.args[-1]
        # Create a new task in the database
        Task.objects.create(title=title, description=description, due_date=due_date)
        update.message.reply_text('✅ Task added successfully!')
    except IndexError:
        # Handle the case where the arguments are incomplete
        update.message.reply_text('❌ Error: Please provide all necessary parameters: /add_task <title> <description> <YYYY-MM-DD>.')


def delete_task(update: Update, context: CallbackContext):
    try:
        task_id = int(context.args[0])
        task = Task.objects.get(id=task_id)
        task.delete()
        
        # Reorder task IDs in the database
        with connection.cursor() as cursor:
            cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'TaskList_task'")
            cursor.execute("VACUUM")

        update.message.reply_text('🗑️ Task deleted successfully!')
    except Task.DoesNotExist:
        # Handle the case where the task does not exist
        update.message.reply_text('❌ Error: Task not found.')
    except (ValueError, IndexError):
        # Handle errors related to invalid ID or missing ID
        update.message.reply_text('❌ Error: Please provide a valid ID: /delete_task <id>.')


def complete_task(update: Update, context: CallbackContext):
    try:
        task_id = int(context.args[0])
        task = Task.objects.get(id=task_id)
        task.completed = True
        task.save()
        update.message.reply_text('✅ Task marked as completed!')
    except Task.DoesNotExist:
        # Handle the case where the task does not exist
        update.message.reply_text('❌ Error: Task not found.')
    except (ValueError, IndexError):
        # Handle errors related to invalid ID or missing ID
        update.message.reply_text('❌ Error: Please provide a valid ID: /complete_task <id>.')


def list_tasks(update: Update, context: CallbackContext):
    tasks = Task.objects.all()
    if tasks:
        message = "📋 Task List:\n"
        for task in tasks:
            status = '✅ Completed' if task.completed else '❌ Not Completed'
            message += (
                f"\n🆔 ID: {task.id}\n"
                f"📌 Title: {task.title}\n"
                f"📝 Description: {task.description}\n"
                f"📅 Due Date: {task.due_date}\n"
                f"🗓️ Created At: {task.created_at}\n"
                f"🔖 Status: {status}\n"
            )
        update.message.reply_text(message)
    else:
        # Handle the case where no tasks are found
        update.message.reply_text('📭 No tasks found.')


def daily_task_notification():
    logger.info("daily_task_notification is being executed")
    try:
        # Create a fake Update and Message object to simulate the /tasks command
        class FakeUpdate:
            message = None
        
        class FakeMessage:
            def reply_text(self, text):
                send_message(text)

        update = FakeUpdate()
        update.message = FakeMessage()

        # Create a fake context and call the list_tasks function
        context = CallbackContext(dispatcher)
        list_tasks(update, context)
        logger.info("Task list has been sent successfully")
    
    except Exception as e:
        # Handle any exceptions that occur during notification
        send_message(f"Error: {str(e)}")
        logger.error(f"Exception occurred: {str(e)}")

# Register command handlers with the dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('add_task', add_task))
dispatcher.add_handler(CommandHandler('delete_task', delete_task))
dispatcher.add_handler(CommandHandler('complete_task', complete_task))
dispatcher.add_handler(CommandHandler('tasks', list_tasks))

def start_bot():
    updater.start_polling()
    logger.info("Bot started and polling for commands")


def stop_bot():
    updater.stop()
    logger.info("Bot stopped")
