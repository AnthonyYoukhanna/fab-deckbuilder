from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
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

    paginator =Paginator(cards,20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'sets':sets,
        'rarities': rarities,
        }
    

    return render(request, 'cards/card_list.html', context)

def card_detail(request, card_id):
    card = get_object_or_404(Card, id=card_id)
    return render(request, 'cards/card_detail.html', 
                  {'card': card})
