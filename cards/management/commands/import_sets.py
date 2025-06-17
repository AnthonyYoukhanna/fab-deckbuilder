import requests
from cards.models import Set, SetPrinting
from django.core.management.base import BaseCommand
from datetime import datetime

class Command(BaseCommand):
    help = 'Imports sets and their printings from the external JSON source'

    def handle(self, *args, **kwargs):
        url = "https://the-fab-cube.github.io/flesh-and-blood-cards/json/english/set.json"
        response = requests.get(url)
        sets_data = response.json()

        for set_data in sets_data:
            set_instance, created = Set.objects.get_or_create(
                set_id=set_data['id'],
                defaults={
                    'unique_id': set_data['unique_id'],
                    'name': set_data['name'],
                }
            )

            for printing in set_data['printings']:

                if 'initial_release_date' in printing and printing['initial_release_date']:
                    initial_release_date_str = printing['initial_release_date']
                    try:
                        initial_release_date = datetime.strptime(initial_release_date_str, "%Y-%m-%dT%H:%M:%S.%fZ").date()
                    except ValueError:
                        continue  # Handle invalid date format
                else:
                    continue  # Set to None if the date is missing

                SetPrinting.objects.get_or_create(
                    unique_id=printing['unique_id'],  # separate unique_id handling
                    set=set_instance,
                    defaults={
                        'edition': printing['edition'],
                        'start_card_id': printing['start_card_id'],
                        'end_card_id': printing['end_card_id'],
                        'initial_release_date': initial_release_date,
                        'out_of_print': printing.get('out_of_print', False),
                        'card_database': printing['card_database'],
                        'product_page': printing['product_page'],
                        'collectors_center': printing.get('collectors_center', ''),
                        'card_gallery': printing.get('card_gallery', ''),
                        'set_logo': printing.get('set_logo', ''),
                        'release_notes': printing.get('release_notes', ''),
                    }
                )

        self.stdout.write(self.style.SUCCESS('Successfully imported sets and printings.'))
