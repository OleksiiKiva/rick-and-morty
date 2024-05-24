from characters.scraper import sync_characters_with_api

from celery import shared_task


@shared_task
def run_synk_with_api() -> None:
    sync_characters_with_api()
