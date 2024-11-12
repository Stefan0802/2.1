from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegisterForm, CustomLoginForm, ApplicationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import PasswordResetQuestionForm
from .models import Application
from  django.views import generic


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'main/register.html', {'form': form})

class ApplicationListView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'application_list'



    def get_queryset(self):
        return Application.objects.order_by('id')

def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        image = request.FILES.get('image')
        if image:
            max_size = 2 * 1024 * 1024
            if image.size > max_size:
                messages.error(request, "Размер изображения не должен превышать 2MB.")
                return render(request, 'create_application.html', {'form': form})

            valid_formats = ['image/jpeg', 'image/png', 'image/gif']
            if image.content_type not in valid_formats:
                messages.error(request, "Допустимые форматы: JPEG, PNG, GIF.")
                return render(request, 'create_application.html', {'form': form})

        if form.is_valid():
            form.save()
            messages.success(request, "Заявка успешно создана.")
            return redirect('application_list')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = ApplicationForm()
    return render(request, 'main/create_application.html', {'form': form})

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

    completed_applications = Application.objects.filter(status='Выполнено').order_by('-created_at')[:4]
    in_progress_count = Application.objects.filter(status='Принято в работу').count()

    return render(request, 'main/home.html', {
        'completed_applications': completed_applications,
        'in_progress_count': in_progress_count,
    })

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

@login_required
def confirm_delete_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)


    if application.user != request.user:
        messages.error(request, "Вы не можете удалить эту заявку.")
        return redirect('application_list')

    return render(request, 'main/confirm_delete.html', {'application': application})

@login_required
def delete_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    if application.user != request.user:
        messages.error(request, "Вы не можете удалить эту заявку.")
        return redirect('application_list')

    if application.status in ['in_progress', 'completed']:
        messages.error(request, "Вы не можете удалить заявку с таким статусом.")
        return redirect('application_list')

    application.delete()
    messages.success(request, "Заявка успешно удалена.")
    return redirect('application_list')