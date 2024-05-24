import requests
from django.conf import settings
from django.db import IntegrityError

from characters.models import Character


def scrape_characters() -> list[Character]:
    next_url_to_scrape = settings.RICK_AND_MORTY_API_CHARACTERS_URL

    characters = []
    while next_url_to_scrape is not None:
        characters_response = requests.get(next_url_to_scrape).json()

        for character_dict in characters_response.get("results"):
            characters.append(
                Character(
                    api_id=character_dict.get("id"),
                    name=character_dict.get("name"),
                    status=character_dict.get("status"),
                    species=character_dict.get("species"),
                    gender=character_dict.get("gender"),
                    image=character_dict.get("image"),
                )
            )

        next_url_to_scrape = characters_response.get("info", {}).get("next", {})

    return characters


def save_characters(characters: list[Character]) -> None:
    for character in characters:
        try:
            character.save()
        except IntegrityError:
            print(f"Character with 'api_id' {character.api_id} already exist in DB")


def sync_characters_with_api() -> None:
    characters = scrape_characters()
    save_characters(characters)
