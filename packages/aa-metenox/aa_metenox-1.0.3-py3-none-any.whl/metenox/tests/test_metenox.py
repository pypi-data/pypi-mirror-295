from unittest import TestCase

from moonmining.models import Moon as MoonMiningMoon
from moonmining.models import MoonProduct

from eveuniverse.models import EveMoon

from allianceauth.eveonline.models import EveCorporationInfo

from metenox.models import HoldingCorporation, Metenox
from metenox.tasks import create_metenox, update_moons_from_moonmining
from metenox.tests.testdata.load_eveuniverse import load_eveuniverse

MOON_ID = 40178441


class TestMetenoxes(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        load_eveuniverse()

    def test_moon_update_when_metenox_created_on_empty_moon(self):
        """
        Check that when a metenox is created on a moon that isn't present in moonmining an update will happen
        if the moon appears in moonmining
        """

        print("--begin--")

        corporation = EveCorporationInfo.objects.create(
            corporation_id=1,
            corporation_name="corporation1",
            corporation_ticker="CORP1",
            member_count=1,
        )
        holding = HoldingCorporation(corporation=corporation)
        holding.save()
        eve_moon = EveMoon.objects.get(id=MOON_ID)

        structure_info = {
            "name": "Metenox1",
            "structure_id": 1,
        }

        location_info = {
            "position": {
                "x": eve_moon.position_x,
                "y": eve_moon.position_y,
                "z": eve_moon.position_z,
            },
            "solar_system_id": eve_moon.eve_planet.eve_solar_system.id,
        }

        create_metenox(
            holding.corporation.corporation_id, structure_info, location_info
        )

        metenox = Metenox.objects.get(structure_id=1)
        self.assertEqual(
            len(metenox.moon.hourly_pull), 0
        )  # checks that the moon is empty
        self.assertEqual(metenox.moon.moonmining_moon, None)

        moon_scan = {
            45490: 0.2809781134,
            45491: 0.2083230466,
            45493: 0.5106988549,
        }

        moonmining_moon, _ = MoonMiningMoon.objects.get_or_create(eve_moon_id=MOON_ID)

        moon_products = [
            MoonProduct(
                moon=moonmining_moon, ore_type_id=ore_type_id, amount=ore_type_amount
            )
            for ore_type_id, ore_type_amount in moon_scan.items()
        ]
        moonmining_moon.update_products(moon_products)

        update_moons_from_moonmining()

        self.assertEqual(
            len(metenox.moon.hourly_pull), 3
        )  # checks that  the moon was updated
