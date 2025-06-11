from django.contrib import admin
from .models import (
    CardType, CardSubType, Keyword, FunctionalKeyword,
    Set, Rarity, Card, CardPrinting, UserCard
)

# Basic inline for printings within Card admin
class CardPrintingInline(admin.TabularInline):
    model = CardPrinting
    extra = 0

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost', 'pitch', 'power', 'defense', 'blitz_legal')
    list_filter = ('types', 'subtypes', 'keywords', 'functional_keywords', 'blitz_legal', 'cc_legal')
    search_fields = ('name', 'description')
    inlines = [CardPrintingInline]
    filter_horizontal = ('types', 'subtypes', 'keywords', 'functional_keywords', 'variations')

@admin.register(CardPrinting)
class CardPrintingAdmin(admin.ModelAdmin):
    list_display = ('card', 'set', 'edition', 'foiling', 'rarity')
    list_filter = ('set', 'foiling', 'rarity')
    search_fields = ('card__name',)

# Register simple models normally
admin.site.register(CardType)
admin.site.register(CardSubType)
admin.site.register(Keyword)
admin.site.register(FunctionalKeyword)
admin.site.register(Set)
admin.site.register(Rarity)
admin.site.register(UserCard)
