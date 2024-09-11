from django.test import TestCase

from metenox.api.fuzzwork import get_type_ids_prices


class TestFuzzWork(TestCase):

    def test_crash_empty_search_query(self):
        """
        With an empty search query the API returns [] instead of a dict.
        This makes the code crash whe calling .items() on the result
        """

        get_type_ids_prices([])
