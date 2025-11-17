from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import models
import json
from .models import Board, Group, Task

def register_view(request):
	# user registartion
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()

    return render(request, 'boards/register.html', {'form': form})

def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'boards/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

@login_required
def home(request):
    boards = request.user.boards.all()
    # render template from the boards app templates directory
    return render(request, 'boards/home.html', {'boards': boards})

@login_required
@require_http_methods(["POST"])
def create_board(request):
    # Create a new board
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        
        if not name:
            return JsonResponse({'success': False, 'error': 'Board name is required'}, status=400)
        
        board = Board.objects.create(
            name=name,
            description=description,
            owner=request.user
        )
        
        return JsonResponse({
            'success': True,
            'board_id': board.id,
            'redirect_url': f'/board/{board.id}/'
        })
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def dashboard(request):
    return render(request, 'boards/dashboard.html')


@login_required
def board_detail(request, board_id):
    try:
        board = Board.objects.get(id=board_id, owner=request.user)
    except Board.DoesNotExist:
        from django.http import Http404
        raise Http404("Board not found")

    # get groups and tasks
    groups = board.groups.prefetch_related('tasks').all()

    return render(request, 'boards/board_detail.html', {
        'board': board,
        'groups': groups,
    })

@login_required
@require_http_methods(["POST"])
def create_group(request, board_id):
    try:
        board = Board.objects.get(id=board_id, owner=request.user)
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        
        if not name:
            return JsonResponse({'success': False, 'error': 'Group name is required'}, status=400)
        
        # Get the highest order value and add 1
        max_order = board.groups.aggregate(models.Max('order'))['order__max'] or 0
        
        group = Group.objects.create(
            name=name,
            board=board,
            order=max_order + 1
        )
        
        return JsonResponse({
            'success': True,
            'group_id': group.id,
            'group_name': group.name
        })
    except Board.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Board not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@require_http_methods(["POST"])
def create_task(request, group_id):
    try:
        group = Group.objects.get(id=group_id, board__owner=request.user)
        data = json.loads(request.body)
        content = data.get('content', '').strip()
        
        if not content:
            return JsonResponse({'success': False, 'error': 'Task content is required'}, status=400)
        
        # Get the highest order value and add 1
        max_order = group.tasks.aggregate(models.Max('order'))['order__max'] or 0
        
        task = Task.objects.create(
            content=content,
            group=group,
            order=max_order + 1
        )
        
        return JsonResponse({
            'success': True,
            'task_id': task.id,
            'task_content': task.content
        })
    except Group.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Group not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@require_http_methods(["POST"])
def update_task(request, task_id):
    task = Task.objects.get(id=task_id, group__board__owner=request.user)
    data = json.loads(request.body)
    task.content = data.get('content', '').strip()
    task.save()
    return JsonResponse({'success': True})

@login_required
@require_http_methods(["POST"])
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id, group__board__owner=request.user)
    task.delete()
    return JsonResponse({'success': True})

@login_required
@require_http_methods(["POST"])
def toggle_task_completed(request, task_id):
    try:
        task = Task.objects.get(id=task_id, group__board__owner=request.user)
        data = json.loads(request.body)
        task.completed = data.get('completed', False)
        task.save()
        return JsonResponse({'success': True, 'completed': task.completed})
    except Task.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Task not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@require_http_methods(["POST"])
def update_board(request, board_id):
    try:
        board = Board.objects.get(id=board_id, owner=request.user)
        
        updated = False
        
        # Handle multipart form data (file upload)
        if request.FILES.get('background_image'):
            board.background_image = request.FILES['background_image']
            updated = True
        
        # Get name from POST data (works for both multipart and JSON)
        name = request.POST.get('name', '').strip()
        if name:
            board.name = name
            updated = True
        
        # Fallback: try JSON body if POST didn't have name
        if not name and request.body:
            try:
                data = json.loads(request.body)
                name = data.get('name', '').strip()
                if name:
                    board.name = name
                    updated = True
            except (json.JSONDecodeError, ValueError):
                pass
        
        # Only save if something was actually updated
        if updated:
            board.save()
        
        bg_url = board.background_image.url if board.background_image else ''
        
        return JsonResponse({
            'success': True,
            'board_name': board.name,
            'background_image': bg_url
        })
    except Board.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Board not found'}, status=404)
    except Exception as e:
        # Log the actual error for debugging
        import traceback
        traceback.print_exc()
        return JsonResponse({'success': False, 'error': str(e)}, status=500)