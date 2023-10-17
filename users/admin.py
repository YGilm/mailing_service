from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'date_joined', 'display_groups')
    list_filter = ('is_active',)

    def display_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])

    display_groups.short_description = 'Группы'
