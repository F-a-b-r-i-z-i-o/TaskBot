import os 
from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
import atexit
import logging

# Set up logging for debugging and tracking
logger = logging.getLogger(__name__)

class TasklistConfig(AppConfig):
    """
    Configuration class for the TaskList Django app.
    
    This class is responsible for setting up the background scheduler and 
    ensuring the Telegram bot starts correctly. It schedules the daily task 
    notification and ensures the bot and scheduler are properly started and stopped.
    """
    name = 'TaskList'

    def ready(self):
        """
        Method called when the Django app is ready. Sets up the bot and the scheduler.

        This method checks if the Django app is being run as the main process, and 
        if so, it starts the bot and the scheduler. The scheduler is configured 
        to run the `daily_task_notification` function at a specific time each day.
        """
        # Avoid double-starting the bot with Django's autoreload
        if os.environ.get('RUN_MAIN', None) != 'true':
            return

       
        import sys
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

        from Bot.telegram_bot import start_bot, stop_bot, daily_task_notification

        start_bot()

        # Initialize the scheduler with the timezone set to 'Europe/Rome'
        scheduler = BackgroundScheduler(timezone=timezone('Europe/Rome'))

        # Schedule the daily task notification 
        job = scheduler.add_job(daily_task_notification, 'cron', hour=17, minute=59)
        logger.info(f"Job {job.id} added to scheduler")


        scheduler.start()
        logger.info("Scheduler started")

        # Ensure the scheduler and bot are properly shut down at exit
        atexit.register(lambda: scheduler.shutdown())
        atexit.register(stop_bot)
