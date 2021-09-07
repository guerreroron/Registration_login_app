from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('first_name','last_name' ,'email', 'rol')
    ordering = ('created_at',)

admin.site.register(User, UserAdmin)
