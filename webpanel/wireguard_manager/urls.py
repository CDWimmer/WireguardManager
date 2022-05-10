from django.urls import path, include, register_converter
from .views.index import IndexView
from .views.network_block_list import NetworkBlockListView
from .views.config import ConfigView
from .models import Device

app_name = "wg_manager"


class DeviceConverter:
    regex = '[0-9]+'

    def to_python(self, value):
        return Device.objects.get(id=value)

    def to_url(self, value):
        return f"{value.id}"


register_converter(DeviceConverter, 'device')

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('blocks/', NetworkBlockListView.as_view(), name='network_block_list'),
    path('device/<device:device>/config/', ConfigView.as_view(), name='device_config'),
    path('account/', include('wireguard_manager.views.account.urls')),
]
