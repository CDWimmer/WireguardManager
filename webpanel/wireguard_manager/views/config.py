from django import views
from django.shortcuts import render
from django.http.response import JsonResponse
from django.http.request import HttpRequest
from ..models import Device, Peering


class ConfigView(views.View):
    def get(self, request: HttpRequest, device: Device):
        peers = Peering.objects.filter(peer_a=device) | Peering.objects.filter(peer_b=device)
        ctx = {
            "this": device,
            "peers": [
                (peering, peering.peer(device)) for peering in peers
            ]
        }

        response = render(request, "wg_manager/config/full.html", context=ctx)
        response["Content-Type"] = "text/plain"
        response["Content-Disposition"] = "inline"
        return response
