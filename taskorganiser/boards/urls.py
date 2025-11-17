from django.urls import path
from . import views

urlpatterns = [
    # root of the site should show the home page
    path('', views.home, name='home'),
    # keep the dashboard route available if needed
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('boards/create/', views.create_board, name='create_board'),
    # also expose singular path used by the frontend JS
    path('board/create/', views.create_board, name='create_board_singular'),
    # board detail view
    path('board/<int:board_id>/', views.board_detail, name='board_detail'),
    # API endpoints for groups and tasks
    path('board/<int:board_id>/group/create/', views.create_group, name='create_group'),
    path('group/<int:group_id>/update/', views.update_group, name='update_group'),
    path('group/<int:group_id>/task/create/', views.create_task, name='create_task'),
    path('task/<int:task_id>/update/', views.update_task, name='update_task'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('task/<int:task_id>/toggle/', views.toggle_task_completed, name='toggle_task_completed'),
    path('board/<int:board_id>/update/', views.update_board, name='update_board'),
]
