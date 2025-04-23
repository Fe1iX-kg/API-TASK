from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'created_at', 'is_completed']
        read_only_fields = ['created_at']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Название задачи не может быть пустым.")
        return value