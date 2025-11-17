from django import forms
from .models import Board, Group, Task

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Board Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Board Description', 'rows': 3}),
        }

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Group Name'}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['content', 'completed']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Task Content', 'rows': 3}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }