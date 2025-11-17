from django.contrib import admin
from .models import Board, Group, Task

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at', 'updated_at')
    list_filter = ('owner', 'created_at')
    search_fields = ('name', 'description')

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'board', 'order', 'created_at')
    list_filter = ('board', 'created_at')
    search_fields = ('name',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('content', 'group', 'completed', 'order', 'created_at')
    list_filter = ('completed', 'group', 'created_at')
    search_fields = ('content',)