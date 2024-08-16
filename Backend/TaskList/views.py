from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task
from .forms import TaskForms

class TaskListView(ListView):
    model = Task
    template_name = 'TaskList/task_list.html'
    context_object_name = 'tasks'

class TaskDetailView(DetailView):
    model = Task
    template_name = 'TaskList/task_detail.html'
    context_object_name = 'task'

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForms
    template_name = 'TaskList/task_edit.html'
    success_url = reverse_lazy('task_list')

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForms
    template_name = 'TaskList/task_edit.html'
    success_url = reverse_lazy('task_list')

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'TaskList/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')
