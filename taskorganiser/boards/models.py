from django.db import models
from django.contrib.auth.models import User

class Board(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    background_image = models.CharField(max_length=500, default='images/background-default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']
    
class Group(models.Model):
    name = models.CharField(max_length=255)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='groups')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.IntegerField(default=0)  # For custom ordering

    def __str__(self):
        return f"{self.name} - {self.board.name}"
    
    class Meta:
        ordering = ['order', 'created_at']
    
class Task(models.Model):
    content = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='tasks')
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.IntegerField(default=0)  # For custom ordering

    def __str__(self):
        return f"{self.content[:50]}"
    
    class Meta:
        ordering = ['order', 'created_at']