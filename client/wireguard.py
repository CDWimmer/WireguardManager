import requests
from time import sleep
import subprocess


class WireGuard:
    def __init__(self, interface='wg0', debug=False):
        self.interface = interface

    def _wg_set(self, obj_name, value):
        pass

    def _wg_remove(self, obj_name, value):
        pass

