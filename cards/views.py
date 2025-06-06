from django.shortcuts import render
from .models import Card, Set, Rarity

# Create your views here.

def card_list(request):
    sort_by = request.GET.get('sort')
    cards = Card.objects.all()

    sets = Set.objects.all()
    rarities = Rarity.objects.all()

    if 'rarity' in request.GET and request.GET['rarity']:
        cards = cards.filter(rarity_id=request.GET['rarity'])
    if 'set' in request.GET and request.GET['set']:
        cards = cards.filter(set_id=request.GET['set'])
    if sort_by in ['name', 'cost', 'pitch']:
        cards = cards.order_by(sort_by)


    return render(request, 'cards/card_list.html', {
        'cards': cards,
        'sets': sets,
        'rarities': rarities,
        })
