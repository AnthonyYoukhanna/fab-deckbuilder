import json
import requests
from django.core.management.base import BaseCommand
from cards.models import (
    Card, CardPrinting, CardType, CardSubType, Keyword,
    FunctionalKeyword, Set, Rarity
)

class Command(BaseCommand):
    help = "Import cards from JSON"

    def handle(self, *args, **kwargs):
        with open("cards.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        print("📥 Starting card import...")

        for entry in data:
            # --- Base Card ---
            unique_id = entry.get("unique_id")
            if not unique_id:
                raise ValueError(f"Missing unique_id for entry: {entry.get('name')}")


            card, card_created = Card.objects.update_or_create(
                unique_id = entry.get("unique_id"),
                defaults={
                    "name": entry.get("name", ""),
                    "pitch": int(entry["pitch"]) if entry.get("pitch", "").isdigit() else None,
                    "cost": entry.get("cost") or None,
                    "power": entry.get("power") or None,
                    "defense": entry.get("defense") or None,
                    "health": entry.get("health") or None,
                    "intelligence": entry.get("intelligence") or None,
                    "arcane": entry.get("arcane") or None,
                    "description": entry.get("functional_text") or None,
                    "type_text": entry.get("type_text") or None,
                    "played_horizontally": entry.get("played_horizontally", False),
                    "is_token": entry.get("is_token", False),
                    "is_starter": entry.get("is_starter", False),
                    "blitz_legal": entry.get("blitz_legal", True),
                    "cc_legal": entry.get("cc_legal", True),
                    "commoner_legal": entry.get("commoner_legal", False),
                    "ll_legal": entry.get("ll_legal", False),
                }
            )
            #print(f"{'🟢 updated' if card_created else '🔵 Skipped'} card: {card.name}")

            # --- Card Types ---
            card.types.clear()
            for type_name in entry.get("types", []):
                card_type, created = CardType.objects.get_or_create(name=type_name)
                card.types.add(card_type)
                if created:
                    print(f"  ➕ Created CardType: {type_name}")

            # --- Subtypes ---
            card.subtypes.clear()
            for subtype_name in entry.get("subtypes", []):
                subtype, created = CardSubType.objects.get_or_create(name=subtype_name)
                card.subtypes.add(subtype)
                if created:
                    print(f"  ➕ Created CardSubType: {subtype_name}")

            # --- Keywords ---
            card.keywords.clear()
            for kw in entry.get("card_keywords", []):
                keyword, created = Keyword.objects.get_or_create(name=kw)
                card.keywords.add(keyword)
                if created:
                    print(f"  ➕ Created Keyword: {kw}")

            # --- Functional Keywords ---
            card.functional_keywords.clear()
            for fkw in entry.get("functional_keywords", []):
                f_keyword, created = FunctionalKeyword.objects.get_or_create(name=fkw)
                card.functional_keywords.add(f_keyword)
                if created:
                    print(f"  ➕ Created FunctionalKeyword: {fkw}")

            # --- Printings ---
            for printing in entry.get("printings", []):
                set_code = printing.get("set_id")
                if not set_code:
                    continue

                set_obj, set_created = Set.objects.get_or_create(
                    code=set_code,
                    defaults={"name": set_code}
                )
                if set_created:
                    print(f"  🗃️ Created Set: {set_code}")

                rarity_name = printing.get("rarity")
                rarity_obj = None
                if rarity_name:
                    rarity_obj, rarity_created = Rarity.objects.get_or_create(name=rarity_name)
                    if rarity_created:
                        print(f"  🏅 Created Rarity: {rarity_name}")

                image_url = printing.get("image_url")
                card_number = printing.get("id")
                edition = printing.get("edition")
                foiling = printing.get("foiling")
                unique_id = printing.get("unique_id")   

                #print(f"Trying: {card.name} [{set_code}] ({foiling}) #{card_number}, {edition}, {rarity_obj}")
                # 🛡️ Guard clause to skip if unique_id already exists
                # if CardPrinting.objects.filter(unique_id=unique_id).exists():
                #     print(f"⚠️ Skipping duplicate unique_id: {unique_id}")
                #     continue

                cp, cp_created = CardPrinting.objects.update_or_create(
                    unique_id = unique_id,
                    defaults = {
                        "art_variation": printing.get("art_variations", ""),
                        "flavour_text": printing.get("flavour_text", ""),
                        "card":card,
                        "set":set_obj,
                        "foiling":foiling,
                        "card_number":card_number or "",
                        "edition":edition or "",
                        # rarity=rarity_obj,
                        # image_url= image_url or "",
                        # tcgplayer_url = printing.get("tcgplayer_url", ""),
                        "artists": printing.get("artists", []) or [],
                    }
                    
                )
                
                #print(f"  {'🖨️ Added' if cp_created else '◽ Skipped'} printing: {card.name} [{set_code}] ({foiling})")
