from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Min
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

    exclude_filter = (
        Q(printings__set__name__icontains='Blitz') | 
        Q(printings__set__name__icontains='Armory') | 
        Q(printings__set__name__icontains='Deck') | 
        Q(printings__set__name__icontains='Promo') | 
        Q(printings__set__name__icontains='Classic') |
        Q(printings__set__name__icontains='Event') | 
        Q(printings__set__name__icontains='Table') | 
        Q(printings__set__name__icontains='Strike') | 
        Q(printings__set__name__icontains='Worlds')
    )

    sort_by = request.GET.get('sort')
    cards = CardPrinting.objects.select_related('card', 'set_printing', 'rarity').all()
    sets = Set.objects.annotate(
        earliest_release=Min('printings__initial_release_date')
        ).exclude(exclude_filter
        ).order_by('earliest_release') #sorts the filtering section by release date
    
    excluded_sets = Set.objects.annotate(
        earliest_release=Min('printings__initial_release_date')
        ).filter(exclude_filter).order_by('earliest_release') #Gets the sets that were filtered out back in
    

    rarities = Rarity.objects.all()
    keywords = Keyword.objects.all()  # Assuming you're filtering by keywords
    foils = CardPrinting.FOIL_CHOICES
    editions = CardPrinting.EDITION_CHOICES

    #Filter out cards from blitz decks and etc from initial page population.
    include_extra = request.GET.get('include_extra', '') == 'on'
    if not include_extra:
        exclude_filter = (
            Q(set_printing__set__name__icontains='Blitz') |
            Q(set_printing__set__name__icontains='Armory') |
            Q(set_printing__set__name__icontains='Deck') |
            Q(set_printing__set__name__icontains='Promo') |
            Q(set_printing__set__name__icontains='Classic') |
            Q(set_printing__set__name__icontains='Event') |
            Q(set_printing__set__name__icontains='Table') |
            Q(set_printing__set__name__icontains='Strike') |
            Q(set_printing__set__name__icontains='Worlds')        
        )
        cards = cards.exclude(exclude_filter)


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
        'excluded_sets': excluded_sets,
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

@require_POST
@login_required
def bulk_add_view(request): #add bulk from sets (theres a button for now)
    set_id = request.GET.get('set_id')

    main_cards = CardPrinting.objects.filter(
        set_printing__set_id=set_id,
        rarity__description__in=['Common', 'Rare'],
        foiling='S'
    )

    for cp in main_cards:
        obj, created = UserCardPrintings.objects.get_or_create(
            user=request.user,
            card_printing=cp,
            defaults={'quantity': 3}
        )
        if not created:
            obj.quantity += 3
            obj.save()

    return JsonResponse({'status': 'ok'})

@login_required
def collection_view(request):
    user_cards = UserCardPrintings.objects.filter(user=request.user).select_related(
        'card_printing__card', 'card_printing__rarity', 'card_printing__set_printing'
    )

    #dynamically update the filter list thing
    owned_set_ids = user_cards.values_list('card_printing__set_printing__set_id', flat=True).distinct()

    main_sets = Set.objects.filter(
        Q(id__in=owned_set_ids) &
        ~Q(name__iregex=r'Blitz|Armory|Deck|Promo|Classic|Event|Table|Strike|Worlds')
    ).annotate(
        earliest_release=Min('printings__initial_release_date')
    ).order_by('earliest_release')

    extra_sets = Set.objects.filter(
        Q(id__in=owned_set_ids) &
        Q(name__iregex=r'Blitz|Armory|Deck|Promo|Classic|Event|Table|Strike|Worlds')
    ).annotate(
        earliest_release=Min('printings__initial_release_date')
    ).order_by('earliest_release')


    # Filtering
    set_ids = request.GET.getlist('set')
    rarity_ids = request.GET.getlist('rarity')
    type_ids = request.GET.getlist('type')

    if set_ids:
        user_cards = user_cards.filter(card_printing__set_printing__set_id__in=set_ids)

    if rarity_ids:
        user_cards = user_cards.filter(card_printing__rarity_id__in=rarity_ids)

    if type_ids:
        user_cards = user_cards.filter(card_printing__card__types__id__in=type_ids).distinct()

    #Search bar
    search_query = request.GET.get('search')
    if search_query:
        user_cards = user_cards.filter(
            Q(card_printing__card__name__icontains=search_query) |
            Q(card_printing__card__keywords__name__icontains=search_query) |
            Q(card_printing__card__types__name__icontains=search_query)
        ).distinct()


    user_cards = user_cards.order_by('card_printing__card__name')  
    paginator = Paginator(user_cards, 25)  # Show 25 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    query = request.GET.get('q')
    if query:
        user_cards = user_cards.filter(card_printing__card__name__icontains=query)

    context = {
        'user_cards': user_cards,
        'main_sets': main_sets,
        'extra_sets': extra_sets,
        'rarities': Rarity.objects.all(),
        'types': CardType.objects.all(),
        'page_obj' : page_obj,
        'request': request,
    }
    return render(request, 'cards/collection.html', context)

