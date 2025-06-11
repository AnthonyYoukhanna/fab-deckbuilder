import json
import os

from django.core.management.base import BaseCommand
from cards.models import (
    Card, CardPrinting, CardType, CardSubType, Keyword,
    Set, Rarity
)


def parse_pitch(pitch_value):
    if pitch_value in (None, '', 'null'):
        return None
    try:
        pitch_int = int(pitch_value)
        return pitch_int if pitch_int in [1, 2, 3] else None
    except ValueError:
        return None


class Command(BaseCommand):
    help = "Import cards from JSON"

    def handle(self, *args, **kwargs):
        with open("cards.json", "r", encoding="utf-8") as f:
            cards_data = json.load(f)

        for item in cards_data:
            # Handle Set
            set_code = item.get('set_id')
            set_name = item.get('set_name', set_code)
            set_obj, _ = Set.objects.get_or_create(code=set_code, defaults={'name': set_name})

            # Handle Rarity
            rarity_name = item.get('rarity')
            rarity_obj = None
            if rarity_name:
                rarity_obj, _ = Rarity.objects.get_or_create(name=rarity_name)

           # Handle Card (core)
            card_id = item.get('id') or f"{item.get('name')}_{item.get('type')}_{item.get('pitch')}"
            card_obj, created = Card.objects.get_or_create(
                unique_id=card_id,
                defaults={
                    'name': item.get('name'),
                    'description': item.get('text'),
                    'type_text': item.get('type'),
                    'cost': item.get('cost') or None,
                    'pitch': parse_pitch(item.get('pitch')),
                    'power': item.get('power') or None,
                    'defense': item.get('defense') or None,
                    'health': item.get('life') or None,
                    'intelligence': item.get('intelligence') or None,
                    'arcane': item.get('intellect') or None,
                    'is_token': item.get('is_token', False),
                    'is_starter': item.get('is_starter', False),
                    'blitz_legal': item.get('blitz_legal', True),
                    'cc_legal': item.get('cc_legal', True),
                    'commoner_legal': item.get('commoner_legal', False),
                    'll_legal': item.get('ll_legal', False),
                }
            )

            if created:
                print(f"Created card: {card_obj.name}")
            else:
                print(f"Skipped existing card: {card_obj.name}")

            # Card Types
            for type_name in item.get('types', []):
                type_obj, _ = CardType.objects.get_or_create(name=type_name)
                card_obj.types.add(type_obj)

            # Card Subtypes
            for subtype_name in item.get('subtypes', []):
                subtype_obj, _ = CardSubType.objects.get_or_create(name=subtype_name)
                card_obj.subtypes.add(subtype_obj)

            # Keywords
            for keyword_name in item.get('keywords', []):
                keyword_obj, _ = Keyword.objects.get_or_create(name=keyword_name)
                card_obj.keywords.add(keyword_obj)

            # Card Printing
            CardPrinting.objects.get_or_create(
                card=card_obj,
                set=set_obj,
                foiling=item.get('foil') or '',
                defaults={
                    'edition': item.get('edition') or '',
                    'rarity': rarity_obj,
                    'image_url': item.get('image_url') or '',
                    'tcgplayer_url': item.get('tcgplayer_url') or '',
                    'artists': item.get('artist') if isinstance(item.get('artist'), list) else [item.get('artist')],
                    'card_number': item.get('number') or '',
                }
            )

        self.stdout.write(self.style.SUCCESS("✅ Card import complete."))
