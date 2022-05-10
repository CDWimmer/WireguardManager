from django.db import models
import secrets
import base64


def new_psk():
    the_bytes = secrets.token_bytes(32)
    return base64.b64encode(the_bytes)


class Peering(models.Model):
    peer_a = models.ForeignKey('Device', on_delete=models.CASCADE, related_name='+')
    peer_b = models.ForeignKey('Device', on_delete=models.CASCADE, related_name='+')

    local_peering = models.BooleanField(default=False)
    pre_shared_key = models.CharField(max_length=50, default=new_psk)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.peer_a == self.peer_b:
            raise ValueError("Peering with self makes no sense")
        try:
            Peering.objects.get(peer_a=self.peer_b, peer_b=self.peer_a)
            raise ValueError("Peering already exists")
        except Peering.DoesNotExist:
            pass
        super().save(force_insert, force_update, using, update_fields)

    def peer(self, me):
        if me == self.peer_a:
            return self.peer_b
        elif me == self.peer_b:
            return self.peer_a
        raise ValueError("Device provided is not part of this peering")

    def __str__(self):
        return f"{self.peer_a} X {self.peer_b}"
