from django.db import models
from django.core.validators import MaxValueValidator
from django.template.engine import Engine
from .network_block import ip_to_int, int_to_ip


default_template_engine = Engine.get_default()


class Device(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    # WireGuard info
    public_key = models.CharField(max_length=50)
    public_endpoint = models.CharField(max_length=64, blank=True, default="")
    local_endpoint = models.CharField(max_length=64, blank=True, default="")
    listen_port = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(65535)
        ],
        default=0
    )
    address_block = models.ForeignKey("NetworkBlock", on_delete=models.CASCADE)
    address = models.GenericIPAddressField(protocol="IPv4")
    other_addresses = models.TextField(blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if ip_to_int(self.address) & ((2**self.address_block.prefix - 1) << (32-self.address_block.prefix)) != ip_to_int(self.address_block.block):
            raise ValueError("Address is not inside the block")
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f"{self.address_block.name}: {self.name}"
