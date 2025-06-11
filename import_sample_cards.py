import json
from cards.models import Card, CardType, CardSubType, Keyword, FunctionalKeyword, Set, Rarity, CardPrinting
from django.db import transaction

with open("sample_cards.json", "r") as f:
    data = json.load(f)

for entry in data:
    with transaction.atomic():
        # Lookup or create related fields
        type_objs = [CardType.objects.get_or_create(name=t)[0] for t in entry.get("types", [])]
        subtype_objs = [CardSubType.objects.get_or_create(name=s)[0] for s in entry.get("subtypes", [])]
        keyword_objs = [Keyword.objects.get_or_create(name=k)[0] for k in entry.get("keywords", [])]
        fkeyword_objs = [FunctionalKeyword.objects.get_or_create(name=k)[0] for k in entry.get("functional_keywords", [])]

        card = Card.objects.create(
            unique_id=entry["unique_id"],
            name=entry["name"],
            description=entry.get("description", ""),
            type_text=entry.get("type_text", ""),
            cost=entry.get("cost"),
            pitch=entry.get("pitch"),
            power=entry.get("power"),
            defense=entry.get("defense"),
            health=entry.get("health"),
            intelligence=entry.get("intelligence"),
            arcane=entry.get("arcane"),
            played_horizontally=entry.get("played_horizontally", False),
            is_token=entry.get("is_token", False),
            is_starter=entry.get("is_starter", False),
            blitz_legal=entry.get("blitz_legal", True),
            cc_legal=entry.get("cc_legal", True),
            commoner_legal=entry.get("commoner_legal", False),
            ll_legal=entry.get("ll_legal", False)
        )
        card.types.set(type_objs)
        card.subtypes.set(subtype_objs)
        card.keywords.set(keyword_objs)
        card.functional_keywords.set(fkeyword_objs)

        print_info = entry["printing"]

        set_obj, _ = Set.objects.get_or_create(name=print_info["set"])
        rarity_obj, _ = Rarity.objects.get_or_create(name=print_info["rarity"])

        CardPrinting.objects.create(
            card=card,
            set=set_obj,
            edition=print_info.get("edition"),
            foiling=print_info.get("foiling"),
            rarity=rarity_obj,
            image_url=print_info["image_url"],
            tcgplayer_url=print_info.get("tcgplayer_url"),
            artists=print_info.get("artists", []),
            card_number=print_info.get("card_number")
        )

print("Import complete.")
