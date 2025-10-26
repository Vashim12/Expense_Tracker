from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Expense

# ---------- Authentication Views ----------

def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        User.objects.create_user(username=username, password=password)
        messages.success(request, "Registration successful! Please login.")
        return redirect('login')

    return render(request, 'register.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


# ---------- Expense Views ----------

@login_required(login_url='login')
def index(request):
    expenses = Expense.objects.filter(user=request.user)
    total = sum(e.amount for e in expenses)
    return render(request, 'index.html', {'expenses': expenses, 'total': total})


@login_required(login_url='login')
def add_expense(request):
    if request.method == 'POST':
        title = request.POST['title']
        category = request.POST['category']
        amount = request.POST['amount']
        Expense.objects.create(title=title, category=category, amount=amount, user=request.user)
        return redirect('index')
    return render(request, 'add_expense.html')


@login_required(login_url='login')
def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    expense.delete()
    return redirect('index')
