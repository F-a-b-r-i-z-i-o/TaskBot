# TaskBot 📋🤖

Welcome to TaskBot! This project is a Django-based task management bot that integrates with Telegram to help you manage your tasks efficiently. Follow the instructions below to set up and run the project.

## Prerequisites 🛠️

Before you begin, ensure you have the following installed on your system:

- **Python 3.8+** 🐍
- **Virtualenv** (optional but recommended) 🌐
- **Django 3.x or 4.x** 🌱
- **Telegram Bot Token** (Create a bot using [BotFather](https://core.telegram.org/bots#botfather) and obtain the token) 🔑

## Installation Steps 🚀

Follow these steps to get the project up and running:

### 1. Clone the Repository 📂

```bash
git clone https://github.com/yourusername/TaskBot.git
cd TaskBot
```

### 2. Create a Virtual Environment 🌐

It's a good practice to create a virtual environment to manage dependencies:

```bash
python3 -m venv env
source env/bin/activate  # On Windows use `env\Scriptsctivate`
```

### 3. Install Dependencies 📦

Install all the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables 🌍

Create a `.env` file in the root directory and add your Telegram bot token and chat ID:

```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

### 5. Run Migrations ⚙️

Prepare the database by running Django migrations:

```bash
python manage.py migrate
```

### 6. Run the Server 🌐

Start the Django development server:

```bash
python manage.py runserver
```

### 7. Start the Bot 🤖

Once the server is running, the bot will start automatically. It will listen for commands and send daily task notifications at the scheduled time (configured to 17:59 by default).

## Usage 📚

### Available Commands 💬

Once the bot is running, you can interact with it using the following commands:

- **/start**: Start the bot and display available commands.
- **/add_task `<title>` `<description>` `<YYYY-MM-DD>`**: Add a new task.
- **/delete_task `<id>`**: Delete a task by its ID.
- **/tasks**: List all tasks.
- **/complete_task `<id>`**: Mark a task as completed.

### Scheduling Notifications ⏰

The bot is configured to send a daily task notification at 10:00 (Europe/Rome timezone). You can modify the time in the `TaskList/apps.py` file:

```python
job = scheduler.add_job(daily_task_notification, 'cron', hour=10, minute=00)
```

Adjust the `hour` and `minute` parameters as needed.

## Troubleshooting & Tips 🛠️

- **Conflict with Bot Instances**: If you encounter a `Conflict: terminated by other getUpdates request` error, ensure that no other instance of the bot is running.
- **Updating Dependencies**: If you add new packages, update the `requirements.txt` file using `pip freeze > requirements.txt`.

## Contributing 🤝

Feel free to fork this repository and submit pull requests if you'd like to contribute to the project. Your help is always appreciated! 🌟

## License 📜

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*Enjoy 2F*
