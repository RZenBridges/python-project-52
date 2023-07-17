from django.contrib import admin
from .models import User


# Register your models here.
@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'date_joined')
    search_fields = ['username', 'first_name', 'last_name', 'date_joined']
    list_filter = (('created_at', admin.DateFieldListFilter), )
