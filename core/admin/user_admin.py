from django.contrib import admin
from core.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'is_staff', 'is_active')
    list_display_links = ('id', 'email', 'username')
    search_fields = ('email', 'username')
    list_filter = ('is_staff', 'is_active')
    list_per_page = 25
