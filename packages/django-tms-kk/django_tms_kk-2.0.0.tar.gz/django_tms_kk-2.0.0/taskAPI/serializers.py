from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['valid_status','title','description','status','valid_priority','priority','due_date','created_at','updated_at']
        