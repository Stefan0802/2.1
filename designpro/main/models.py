from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.timezone import now
from django.core.validators import FileExtensionValidator

class CustomUser(AbstractUser):
    security_question = models.CharField(max_length=255, blank=True)
    security_answer = models.CharField(max_length=255, blank=True)
    login_count = models.IntegerField(default=0)
    last_login_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.login_count = 0
        super().save(*args, **kwargs)

    def increment_login_count(self):
        self.login_count += 1
        self.last_login_date = now()
        self.save()

STATUS_CHOICES = (
    ('Новая', 'Новая'),
    ('Принято в работу', 'Принято в работу'),
    ('Выполнено', 'Выполнено'),
)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Application(models.Model):
    title_application = models.CharField(max_length=255, blank=True)
    description_application = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)
    image = models.ImageField(upload_to='application/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Новая')

    comment = models.TextField(blank=True)
    design_image = models.ImageField(upload_to='designs/', null=True, blank=True)

    def __str__(self):
        return f"Заявка #{self.id}"

    def can_be_deleted(self, user):
        """Проверяет, может ли пользователь удалить заявку."""
        return self.status == 'Новая' and self.user == user