
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Cususer, Candidate

@admin.register(Cususer)
class CususerAdmin(UserAdmin):
    # Optionally, customize the admin display
    list_display = ('username', 'email', 'is_student', 'is_recruiter', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_student', 'is_recruiter')}),
    )

admin.site.register(Candidate)