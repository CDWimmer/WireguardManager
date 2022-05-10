from .login_required import LoginRequiredView
from django.shortcuts import render
from ..models import NetworkBlock


class NetworkBlockListView(LoginRequiredView):
    def get(self, request):
        ctx = {
            "blocks": NetworkBlock.objects.all(),
        }
        return render(request, "wg_manager/network_block_list.html", context=ctx)
