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
    name = models.CharField(max_length=32)
    block = models.GenericIPAddressField(protocol='IPv4', unique=True)
    prefix = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(32),
            MinValueValidator(8)
        ]
    )

    description = models.TextField(blank=True, default="")

    admins = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return f"{self.block}/{self.prefix}: {self.name}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.block = int_to_ip(ip_to_int(self.block) & ((2**self.prefix - 1) << (32-self.prefix)))

        # Check the block is part of the IANA assigned private networks blocks
        for private_block_start, cidr in iana_private_blocks:
            if ip_to_int(self.block) & ((2**cidr - 1) << (32-cidr)) == private_block_start:
                break
        else:
            raise ValueError("You entered a block that is not in the list of IANA assigned private blocks")

        # Check the block is not part of any other existing block
        # This is an expensive check and needs to be optimised if possible
        other_blocks = NetworkBlock.objects.exclude(id=self.id)
        for other_block in other_blocks:
            min_cidr = min(other_block.prefix, self.prefix)
            if ip_to_int(self.block) & ((2**min_cidr - 1) << (32-min_cidr)) == ip_to_int(other_block.block) & ((2**min_cidr - 1) << (32-min_cidr)):
                raise ValueError(f"You entered a block that overlaps the {other_block} block")
        super().save(force_insert, force_update, using, update_fields)

