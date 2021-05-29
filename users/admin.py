from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    """Администрирование ролей."""
    list_display = ("role",)


admin.site.register(User, UserAdmin)
