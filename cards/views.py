from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import QueryDict, JsonResponse
from .models import Card, Set, Rarity, CardPrinting, UserCardPrintings   

# Create your views here.

def card_list(request):
    sort_by = request.GET.get('sort')
    cards = CardPrinting.objects.select_related('card', 'set', 'rarity').all()
    sets = Set.objects.all()
    rarities = Rarity.objects.all()
    user_quantities = {}
    if request.user.is_authenticated:
        user_quantities = {
            u.card_printing.unique_id: u.quantity
            for u in UserCardPrintings.objects.filter(user=request.user)
        }


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
        'quantities': user_quantities,
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

#this is for incrimenting users collection

@login_required
def increment_card(request):
    if request.method == 'POST':
        unique_id = request.POST.get('unique_id')
        try:
            printing = CardPrinting.objects.get(unique_id=unique_id)
            user_card, created = UserCardPrintings.objects.get_or_create(user=request.user, card_printing=printing)
            user_card.quantity += 1
            user_card.save()
            return JsonResponse({'quantity': user_card.quantity})
        except CardPrinting.DoesNotExist:
            return JsonResponse({'error': 'Card printing not found.'}, status=404)
    return JsonResponse({'error': 'Invalid request.'}, status=400)