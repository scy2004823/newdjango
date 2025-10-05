from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Habit, HabitLog
from .forms import HabitForm, LogForm
from django.contrib import messages
from django.utils import timezone

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('habits:index')
        messages.error(request, 'Invalid credentials')
    return render(request, 'habits/login.html')

def logout_view(request):
    logout(request)
    return redirect('habits:index')

@login_required(login_url='/accounts/login/')
def index(request):
    habits = Habit.objects.filter(owner=request.user)
    recent_logs = HabitLog.objects.filter(habit__owner=request.user)[:10]
    return render(request, 'habits/index.html', {'habits': habits, 'recent_logs': recent_logs})

@login_required(login_url='/accounts/login/')
def create_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            h = form.save(commit=False)
            h.owner = request.user
            h.save()
            messages.success(request, 'Habit created')
            return redirect('habits:index')
    else:
        form = HabitForm()
    return render(request, 'habits/create_habit.html', {'form': form})

@login_required(login_url='/accounts/login/')
def habit_detail(request, pk):
    habit = get_object_or_404(Habit, pk=pk, owner=request.user)
    logs = habit.logs.all()
    return render(request, 'habits/habit_detail.html', {'habit': habit, 'logs': logs})

@login_required(login_url='/accounts/login/')
def log_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = LogForm(request.POST)
        if form.is_valid():
            log, created = HabitLog.objects.update_or_create(habit=habit, date=form.cleaned_data['date'], defaults={'completed': form.cleaned_data['completed'], 'notes': form.cleaned_data['notes']})
            messages.success(request, 'Log saved')
            return redirect('habits:habit_detail', pk=pk)
    else:
        form = LogForm(initial={'date': timezone.localdate()})
    return render(request, 'habits/log_habit.html', {'form': form, 'habit': habit})

@login_required(login_url='/accounts/login/')
def delete_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk, owner=request.user)
    habit.delete()
    messages.success(request, 'Habit deleted')
    return redirect('habits:index')