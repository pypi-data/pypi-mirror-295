import unittest

from metenox.models import EveTypePrice


class TestPrices(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # load_eveuniverse()

    def test_fuel_block_price_not_return_none(self):
        """In case fuel block prices aren't in the database return 0 instead of None"""

        fuel_block_price = EveTypePrice.get_fuel_block_price()

        self.assertIsNotNone(fuel_block_price)
        self.assertEqual(fuel_block_price, 0.0)

    def test_get_price_on_empty_db(self):
        """If no prices are present in the database 0 should be returned instead of anything else"""

        magmatic_price = EveTypePrice.get_magmatic_gases_price()

        self.assertIsNotNone(magmatic_price)
        self.assertEqual(magmatic_price, 0.0)
