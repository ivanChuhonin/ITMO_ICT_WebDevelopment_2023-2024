from django.contrib import admin
from django.contrib.auth.models import User

from .models import Hotel, Room, Guest


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_superuser', 'is_verified')


admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Guest, UserAdmin)
