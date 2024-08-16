import pytest
from unittest.mock import patch, MagicMock
from telegram import Update, Bot, Message, User, Chat
from telegram.ext import CallbackContext
from datetime import date
from TaskList.models import Task
from Backend.Bot.telegram_bot import start, add_task, delete_task, list_tasks, daily_task_notification

@pytest.fixture
def mock_update():
    user = User(id=1, first_name='Test', is_bot=False)
    chat = Chat(id=1, type='private')
    message = Message(message_id=1, from_user=user, chat=chat, date=date.today(), text='')
    return Update(update_id=1, message=message)

@pytest.fixture
def mock_context():
    return CallbackContext(dispatcher=MagicMock())

@pytest.mark.django_db
def test_start_command(mock_update, mock_context):
    mock_update.message.text = '/start'
    start(mock_update, mock_context)
    assert mock_update.message.reply_text.called
    mock_update.message.reply_text.assert_called_once_with(
        '👋 Hello! You can manage your tasks with the following commands:\n'
        '/add_task <title> <description> <YYYY-MM-DD> - Add a new task\n'
        '/delete_task <id> - Delete a task by ID\n'
        '/tasks - List all tasks'
    )

@pytest.mark.django_db
def test_add_task_command(mock_update, mock_context):
    mock_update.message.text = '/add_task TestTitle TestDescription 2024-08-06'
    mock_context.args = ['TestTitle', 'TestDescription', '2024-08-06']
    add_task(mock_update, mock_context)
    assert Task.objects.filter(title='TestTitle').exists()
    assert mock_update.message.reply_text.called
    mock_update.message.reply_text.assert_called_once_with('✅ Task added successfully!')

@pytest.mark.django_db
def test_delete_task_command(mock_update, mock_context):
    task = Task.objects.create(title='TestTitle', description='TestDescription', due_date='2024-08-06')
    mock_update.message.text = f'/delete_task {task.id}'
    mock_context.args = [str(task.id)]
    delete_task(mock_update, mock_context)
    assert not Task.objects.filter(id=task.id).exists()
    assert mock_update.message.reply_text.called
    mock_update.message.reply_text.assert_called_once_with('🗑️ Task deleted successfully!')

@pytest.mark.django_db
def test_list_tasks_command(mock_update, mock_context):
    Task.objects.create(title='TestTitle1', description='TestDescription1', due_date='2024-08-06')
    Task.objects.create(title='TestTitle2', description='TestDescription2', due_date='2024-08-07')
    mock_update.message.text = '/tasks'
    list_tasks(mock_update, mock_context)
    assert mock_update.message.reply_text.called
    response_text = mock_update.message.reply_text.call_args[0][0]
    assert '📋 Task List:\n' in response_text
    assert 'TestTitle1' in response_text
    assert 'TestTitle2' in response_text

@patch('Backend.Bot.telegram_bot.send_message')
@pytest.mark.django_db
def test_daily_task_notification(mock_send_message):
    Task.objects.create(title='TestTitle', description='TestDescription', due_date=date.today())
    daily_task_notification()
    assert mock_send_message.called
    message = mock_send_message.call_args[0][0]
    assert '📅 Daily Tasks:\n' in message
    assert 'TestTitle' in message
    assert 'TestDescription' in message
