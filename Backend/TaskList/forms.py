from django import forms 
from .models import Task

class TaskForms(forms.ModelForm):
    class Meta: 
        model = Task
        fields = ['title', 'description', 'due_date', 'completed']