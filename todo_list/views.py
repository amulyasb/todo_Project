from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from todo_list.models import todo
from django.utils import timezone


# Create your views here.
def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if User.objects.filter(username = username).exists():
            messages.error(request, "username already existed!")
            return redirect('user_register')
        else:
            if password == confirm_password:
                User.objects.create_user(username=username, password=password)
                return redirect('user_login')
            else:
                messages.error(request,"password need to be matched")
                return redirect('user_register')
            
    return render(request, "registration/register.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('todo_list_main')
        else:
            messages.error(request, "user not found")
            return redirect('user_login')
    return render(request, "registration/login.html")

def todo_list_main(request):
    user_Todo = todo.objects.filter(user=request.user).order_by("-id")

    data={
        'user_Todo': user_Todo,
    }


    return render(request, "core/todo_list_main.html", data)

def add_todo(request):
    if request.method == "POST":
        title = request.POST.get("title")
        desc = request.POST.get("desc")

        if title and desc:
            new_todo = todo.objects.create(
                user=request.user, 
                title=title, 
                desc=desc
                )
            new_todo.save()
            messages.success(request, "Successfully add task")
            return redirect('todo_list_main')
        else:
            messages.error(request, 'requried all fields ')
            return redirect('todo_list_main')
        
def delete_todo(request, todo_id):
    todo_item = todo.objects.get( id=todo_id, user=request.user)

    if request.method == "POST":
        todo_item.delete()  
        messages.success(request, "Item deleted successfully")
    
    return redirect('todo_list_main')


def done_todo(request, todo_id):
    todo_item = todo.objects.get(id=todo_id, user=request.user)

    if request.method == "POST":
        if not todo_item.completed:
            todo_item.completed = True
            todo_item.completed_at = timezone.now()
            todo_item.save()
            return redirect('todo_list_main')
    return redirect('todo_list_main')


def update_profile(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = request.user

        # Check if a new username is provided
        # if username and username != user.username:
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("todo_list_main")
        else:
            user.username = username
        
        # Update password if provided
        if password:
            user.set_password(password)  # Use set_password to hash the password

        user.save()
        return redirect("todo_list_main")
    return render(request, "core/todo_list_main.html")

