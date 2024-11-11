from django.contrib.auth.models import AbstractUser , Group, Permission
from django.db import models
from django.utils.timezone import now

class CustomUser (AbstractUser ):
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

