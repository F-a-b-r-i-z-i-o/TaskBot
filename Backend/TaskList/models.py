from django.db import models

class Task(models.Model): 
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['due_date']