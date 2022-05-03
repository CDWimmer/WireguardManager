from django.urls import path, include
from .views.index import IndexView

app_name = "wg_manager"

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('account/', include('wireguard_manager.views.account.urls')),
]
