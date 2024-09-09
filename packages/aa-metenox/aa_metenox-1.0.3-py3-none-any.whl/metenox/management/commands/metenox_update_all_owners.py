from django.core.management.base import BaseCommand

from allianceauth.services.hooks import get_extension_logger

from metenox import tasks

logger = get_extension_logger(__name__)


class Command(BaseCommand):
    help = "Checks all metenox owners and update their Metenoxes"

    def handle(self, *args, **options):
        logger.info("Initiating holding update tasks")
        tasks.update_all_holdings.delay()
