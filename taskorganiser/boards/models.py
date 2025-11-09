from django.db import models
from django.contrib.auth.models import User

class Board(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')

    def __str__(self):
        return self.name
    
class Group(models.Model):
    name = models.CharField(max_length=255)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='groups')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return f"{self.name}, {self.board.name}"
    
class Task(models.Model):
    content = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='tasks')
    completed = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return f"{self.content}"