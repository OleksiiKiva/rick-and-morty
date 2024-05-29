from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from characters.models import Character
from characters.serializers import CharacterSerializer

CHARACTER_URL = reverse("characters:character-list")
# RANDOM_URL = reverse("character:character-list")


def sample_character(**params):
    defaults = {
        "api_id": "1",
        "name": "Rick Sanchez",
        "status": "Alive",
        "species": "Human",
        "gender": "Male",
        "image": "https://1.png",
    }
    defaults.update(params)

    return Character.objects.create(**defaults)


class CharacterApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.character = sample_character()

    def test_filter_characters_by_name(self):
        another_character = sample_character(
            api_id=2,
            name="Test Name",
            image="http://2.png",
        )

        res_without_filter = self.client.get(CHARACTER_URL)
        res_with_filter = self.client.get(CHARACTER_URL, {"name": "Test Name"})

        serializer_with_default_name = CharacterSerializer(self.character)
        serializer_with_test_name = CharacterSerializer(another_character)

        self.assertEqual(res_without_filter.status_code, status.HTTP_200_OK)
        self.assertEqual(res_with_filter.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_with_test_name.data, res_with_filter.data)
        self.assertNotIn(serializer_with_default_name.data, res_with_filter.data)
        self.assertEqual(len(res_without_filter.data), 2)
        self.assertEqual(len(res_with_filter.data), 1)
