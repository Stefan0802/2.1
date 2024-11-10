
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegisterForm, CustomLoginForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('profile')  # Перенаправление на страницу профиля
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'main/profile.html', {'user': request.user})


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)  # Передаем request и data
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Перенаправляем на страницу профиля
    else:
        form = CustomLoginForm()
    return render(request, 'main/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)  # Завершаем сессию пользователя
    return redirect('login')

@login_required
def home_view(request):
    return render(request, 'main/home.html')