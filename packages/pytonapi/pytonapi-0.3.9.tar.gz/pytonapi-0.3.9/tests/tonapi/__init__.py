from unittest import TestCase

from pytonapi import Tonapi

API_KEY = "AE33EX7DNCVC7JAAAAABVSF7O6YWCTGMYMDXSDQYUCV2UUO5AI35QXNTQAWGXEGYPJ2BD5I"


class TestTonapi(TestCase):

    def setUp(self) -> None:
        self.tonapi = Tonapi(api_key=API_KEY, max_retries=10, debug=True)
