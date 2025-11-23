from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Language, Goal, Interest, UserLanguage

class UserLanguageInline(admin.TabularInline):
    model = UserLanguage
    extra = 1

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'username', 'native_language', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Profile Info', {'fields': ('avatar', 'bio', 'birth_date', 'native_language', 'timezone', 'goals', 'interests')}),
    )
    inlines = [UserLanguageInline]

admin.site.register(User, CustomUserAdmin)
admin.site.register(Language)
admin.site.register(Goal)
admin.site.register(Interest)
