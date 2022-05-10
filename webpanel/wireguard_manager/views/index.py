from .login_required import LoginRequiredView
from django.shortcuts import render
from ..models import Peering, Device, NetworkBlock


class IndexView(LoginRequiredView):
    def get(self, request):
        ctx = {
            "blocks_count": NetworkBlock.objects.count(),
            "peering_count": Peering.objects.count(),
            "device_count": Device.objects.count(),
        }
        return render(request, 'wg_manager/index.html', context=ctx)
