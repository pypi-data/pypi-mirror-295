from unittest import IsolatedAsyncioTestCase

from pytonapi import AsyncTonapi

API_KEY = "AE33EX7DNCVC7JAAAAABVSF7O6YWCTGMYMDXSDQYUCV2UUO5AI35QXNTQAWGXEGYPJ2BD5I"


class TestAsyncTonapi(IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.tonapi = AsyncTonapi(api_key=API_KEY, max_retries=10, debug=True)
