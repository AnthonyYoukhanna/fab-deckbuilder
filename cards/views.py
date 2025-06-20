from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import QueryDict, JsonResponse
from .models import Card, Set, Rarity, CardPrinting, UserCardPrintings, SetPrinting, CardType, Keyword

# Create your views here.
from django.db.models import Q
from django.shortcuts import render
from .models import CardPrinting, Rarity, Set, Keyword, CardSubType, CardType

def card_list(request):
    sort_by = request.GET.get('sort')
    cards = CardPrinting.objects.select_related('card', 'set_printing', 'rarity').all()
    sets = Set.objects.all()
    rarities = Rarity.objects.all()
    keywords = Keyword.objects.all()  # Assuming you're filtering by keywords
    foils = CardPrinting.FOIL_CHOICES
    editions = CardPrinting.EDITION_CHOICES

    # Get user quantities if logged in
    user_quantities = {}
    if request.user.is_authenticated:
        user_quantities = {
            u.card_printing.unique_id: u.quantity
            for u in UserCardPrintings.objects.filter(user=request.user)
        }

    # Filtering
    if 'rarity' in request.GET and request.GET['rarity']:
        cards = cards.filter(rarity_id=request.GET['rarity'])

    if 'set' in request.GET and request.GET['set']:
        cards = cards.filter(set_printing__set__id=request.GET['set'])

    if 'keywords' in request.GET and request.GET['keywords']:
        keyword_filters = request.GET.getlist('keywords')
        cards = cards.filter(card__keywords__id__in=keyword_filters)

    if 'foils' in request.GET and request.GET['foils']:
        foiling_filters = request.GET.getlist('foils')
        cards = cards.filter(foiling__in=foiling_filters)

    if 'editions' in request.GET and request.GET['editions']:
        edition_filters = request.GET.getlist('editions')
        cards = cards.filter(edition__in=edition_filters)

    if sort_by in ['name', 'cost', 'pitch']:
        sort_map = {
            'name': 'card__name',
            'cost': 'card__cost',
            'pitch': 'card__pitch',
        }
        cards = cards.order_by(sort_map[sort_by])

    # Pagination
    paginator = Paginator(cards, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Build query string for filters
    query_dict = request.GET.copy()
    if 'page' in query_dict:
        query_dict.pop('page')
    query_string = query_dict.urlencode()

    context = {
        'page_obj': page_obj,
        'sets': sets,
        'rarities': rarities,
        'keywords': keywords,
        'foils': foils,
        'editions': editions,
        'query_string': query_string,
        'quantities': user_quantities,
    }

    return render(request, 'cards/card_list.html', context)


def card_detail(request, card_id):
    card = get_object_or_404(Card, id=card_id)
    return render(request, 'cards/card_detail.html', 
                  {'card': card})

def card_printing_detail(request, unique_id):
    printing = get_object_or_404(CardPrinting.objects.select_related('set_printing'),  unique_id=unique_id)
    other_printings = CardPrinting.objects.select_related('set_printing').filter(card=printing.card).exclude(id=printing.id)
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