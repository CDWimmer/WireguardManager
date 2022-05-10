from django.contrib import admin
from .models import NetworkBlock, Device, Peering


@admin.register(NetworkBlock)
class NetworkBlockAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_staff

    def has_change_permission(self, request, obj: Device = None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return False
        if request.user in obj.address_block.admins:
            return True
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return False
        if request.user in obj.address_block.admins:
            return True
        return False


@admin.register(Peering)
class PeeringAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff
