from django.db import models

class Task(models.Model):
    valid_status = [('To Do','To Do'),('In Progress','In Progress'), ('Completed','Completed')]
    title = models.CharField(max_length=40)
    description = models.TextField()
    status = models.CharField(max_length=15,choices=valid_status,null=False)
    valid_priority = [('l','Low'),('m','Medium'),('h','High')]
    priority = models.CharField(max_length=10,choices=valid_priority, null=False)
    due_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_created=True)

