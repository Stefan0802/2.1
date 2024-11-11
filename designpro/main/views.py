from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegisterForm, CustomLoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import PasswordResetQuestionForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'main/user_profile.html', {'user': request.user})


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                user.increment_login_count()
                login(request, user)
                return redirect('home')
    else:
        form = CustomLoginForm()
    return render(request, 'main/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    return render(request, 'main/home.html', {'user': request.user})

User  = get_user_model()

def password_reset_question(request):
    if request.method == 'POST':
        form = PasswordResetQuestionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            security_answer = form.cleaned_data['security_answer']
            try:
                user = User.objects.get(username=username)

                if user.security_answer == security_answer:

                    return render(request, 'main/user_reset.html', {'user': user})
                else:
                    messages.error(request, "Неверный ответ на секретный вопрос.")
            except User.DoesNotExist:
                messages.error(request, "Пользователь с таким именем не найден.")
    else:
        form = PasswordResetQuestionForm()

    return render(request, 'main/password_reset_question.html', {'form': form})