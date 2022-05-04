from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
import socket
import struct


def ip_to_int(ip):
    packed_ip = socket.inet_aton(ip)
    return struct.unpack("!L", packed_ip)[0]


def int_to_ip(integer):
    return socket.inet_ntoa(struct.pack("!L", integer))


iana_private_blocks = [
    (ip_to_int("10.0.0.0"), 8),
    (ip_to_int("172.16.0.0"), 12),
    (ip_to_int("192.168.0.0"), 16)
]


class NetworkBlock(models.Model):
    block = models.GenericIPAddressField(protocol='IPv4', unique=True)
    prefix = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(32),
            MinValueValidator(8)
        ]
    )

    description = models.TextField(blank=True, default="")

    admins = models.ManyToManyField(settings.AUTH_USER_MODEL, default=None)

    def __str__(self):
        return f"{self.block}/{self.prefix}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.block = int_to_ip(ip_to_int(self.block) & ((2**self.prefix - 1) << (32-self.prefix)))

        for private_block_start, cidr in iana_private_blocks:
            if ip_to_int(self.block) & ((2**cidr - 1) << (32-cidr)) == private_block_start:
                break
        else:
            raise ValueError("You entered a block that is not in the list of IANA assigned private blocks")
        super().save(force_insert, force_update, using, update_fields)

