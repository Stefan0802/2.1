from django.contrib import admin
from .models import CustomUser, Category, Application


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')
    ordering = ('username',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_active=True)



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category)
admin.site.register(Application)