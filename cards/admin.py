from django.contrib import admin
from .models import (
    CardType, CardSubType, Keyword, FunctionalKeyword,
    Set, Rarity, Card, CardPrinting, UserCardPrintings,SetPrinting,
    
)

# Basic inline for printings within Card admin
class CardPrintingInline(admin.TabularInline):
    model = CardPrinting
    extra = 0

class SetPrintingInline(admin.TabularInline):
    model = SetPrinting
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
    list_display = ('card', 'set_printing', 'edition', 'foiling', 'rarity')
    list_filter = ('set_printing', 'foiling', 'rarity')
    search_fields = ('card__name',)

@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ('name', 'set_id', 'unique_id')
    inlines = [SetPrintingInline]

# Register simple models normally
admin.site.register(CardType)
admin.site.register(CardSubType)
admin.site.register(Keyword)
admin.site.register(FunctionalKeyword)
#admin.site.register(Set)
admin.site.register(Rarity)
admin.site.register(UserCardPrintings)
admin.site.register(SetPrinting)
