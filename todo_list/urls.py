from django.contrib import admin
from django.urls import path, include
from todo_list import views

urlpatterns = [
    path('register/', views.user_register, name="user_register"),
    path('login/', views.user_login, name="user_login"),
    path('todo/', views.todo_list_main, name="todo_list_main"),
    path('todo_add/', views.add_todo, name="add_todo"),
    path('todo_delete/<int:todo_id>', views.delete_todo, name="delete_todo"),
    path('todo_done/<int:todo_id>', views.done_todo, name="done_todo"),
    path('update_profile/', views.update_profile, name="update_profile"),
]