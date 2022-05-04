from django.contrib import admin
from .models import NetworkBlock


@admin.register(NetworkBlock)
class NetworkBlockAdmin(admin.ModelAdmin):
    pass
