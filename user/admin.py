from django.contrib import admin
from .models import User, Notes

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'avatar')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('is_staff', 'is_active')
    readonly_fields = ('date_joined', 'last_login')

@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = ('description', 'owner')
    search_fields = ('description', 'owner__username')
    list_filter = ('owner',)
