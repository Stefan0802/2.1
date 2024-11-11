from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth import get_user_model

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')
    security_question = forms.CharField(max_length=255, required=True, label='Контрольный вопрос')
    security_answer = forms.CharField(max_length=255, widget=forms.PasswordInput, required=True, label='Ответ на контрольный вопрос')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'security_question', 'security_answer']

    def save(self, commit=True):
        user = super().save(commit=False)

        user.security_question = self.cleaned_data['security_question']
        user.security_answer = self.cleaned_data['security_answer']

class CustomLoginForm(AuthenticationForm):
    class Meta:
        model = AuthenticationForm
        fields = ('username', 'password')


User  = get_user_model()

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