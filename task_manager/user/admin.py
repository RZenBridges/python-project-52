from django.contrib import admin
from .models import User


# Register your models here.
@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'created_at')
    search_fields = ['username', 'first_name', 'last_name', 'created_at']
    list_filter = (('created_at', admin.DateFieldListFilter), )
