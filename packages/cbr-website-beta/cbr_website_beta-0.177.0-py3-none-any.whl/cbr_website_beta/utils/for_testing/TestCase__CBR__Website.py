from unittest import TestCase

from cbr_website_beta.cbr__fastapi.CBR__Fast_API import cbr_fast_api
from cbr_website_beta.cbr__fastapi.CBR__Fast_API__Client import CBR__Fast_API__Client


class TestCase__CBR__Website(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.client       = CBR__Fast_API__Client()
        cls.cbr_fast_api = cbr_fast_api
        cls.cbr_athena   = cls.cbr_fast_api.cbr__athena()



