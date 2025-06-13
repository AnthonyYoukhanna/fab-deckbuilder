from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import QueryDict
from .models import Card, Set, Rarity, CardPrinting

# Create your views here.

def card_list(request):
    sort_by = request.GET.get('sort')
    cards = CardPrinting.objects.select_related('card', 'set', 'rarity').all()
    sets = Set.objects.all()
    rarities = Rarity.objects.all()

    if 'rarity' in request.GET and request.GET['rarity']:
        cards = cards.filter(rarity_id=request.GET['rarity'])
    if 'set' in request.GET and request.GET['set']:
        cards = cards.filter(set_id=request.GET['set'])
    if sort_by in ['name', 'cost', 'pitch']:
        sort_map = {
            'name': 'card__name',
            'cost': 'card__cost',
            'pitch': 'card__pitch',
        }
        cards = cards.order_by(sort_map[sort_by])

    paginator =Paginator(cards,25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    query_dict = request.GET.copy()
    if 'page' in query_dict:
        query_dict.pop('page')
    query_string = query_dict.urlencode()

    context = {
        'page_obj': page_obj,
        'sets':sets,
        'rarities': rarities,
        'query_string':query_string,
        }
    

    return render(request, 'cards/card_list.html', context)

def card_detail(request, card_id):
    card = get_object_or_404(Card, id=card_id)
    return render(request, 'cards/card_detail.html', 
                  {'card': card})

def card_printing_detail(request, unique_id):
    printing = get_object_or_404(CardPrinting, unique_id=unique_id)
    other_printings = CardPrinting.objects.filter(card=printing.card).exclude(id=printing.id)
    return render(request, 'cards/printing_detail.html', {
        'printing': printing,
        'other_printings': other_printings,
        })
