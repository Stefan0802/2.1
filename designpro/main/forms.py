from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth import get_user_model
from .models import Application, Category, CustomUser

User  = get_user_model()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')
    security_question = forms.CharField(max_length=255, required=True, label='Контрольный вопрос')
    security_answer = forms.CharField(max_length=255, widget=forms.PasswordInput, required=True, label='Ответ на контрольный вопрос')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'security_question', 'security_answer']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.security_question = self.cleaned_data['security_question']
        user.security_answer = self.cleaned_data['security_answer']
        if commit:
            user.save()
        return user

class CustomLoginForm(AuthenticationForm):
    class Meta:
        model = AuthenticationForm
        fields = ('username', 'password')

class PasswordResetQuestionForm(forms.Form):
    username = forms.CharField(max_length=150, label="Имя пользователя")
    security_answer = forms.CharField(max_length=255, label="Ответ на секретный вопрос")

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        security_answer = cleaned_data.get("security_answer")

        if username and security_answer:
            try:
                user = User.objects.get(username=username)
                if user.security_answer != security_answer:
                    raise forms.ValidationError("Неверный ответ на секретный вопрос.")
            except User.DoesNotExist:
                raise forms.ValidationError("Пользователь с таким именем не найден.")


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['title_application', 'description_application', 'category', 'image']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        if user is not None:
            self.instance.user = user

class ChangeStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status', 'image', 'comment']

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        image = cleaned_data.get("image")
        comment = cleaned_data.get("comment")

        if status == 'Выполнено' and not image:
            self.add_error('image', 'Необходимо прикрепить изображение дизайна.')

        if status == 'Принято в работу' and not comment:
            self.add_error('comment', 'Необходимо указать комментарий.')

        return cleaned_data

from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']