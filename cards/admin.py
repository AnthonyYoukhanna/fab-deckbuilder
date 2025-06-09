from django.contrib import admin
from .models import Card, Set, Rarity, UserCard
from .models import CardSubType, CardType, Keyword
# Register your models here.

class CardTypeFilter(admin.SimpleListFilter):
    title = 'Card Type'
    parameter_name = 'card_type'

    def lookups(self, request, model_admin):
        return [(ct.id, ct.name) for ct in CardType.objects.all()]
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(types__id=self.value())
        return queryset

class UserCardAdmin(admin.ModelAdmin):
    list_display = ('user', 'card', 'quantity')
    list_filter = ('user', 'card')
    search_fields = (
        'user__username',
        'card__name',
        'card__type__name',
        'card__keywords__name',
        )
    autocomplete_fields = ['user', 'card']

class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'rarity', 'set', 'foil', 'pitch')
    list_filter = (CardTypeFilter, 'rarity', 'set', 'foil', 'pitch')
    search_fields = ('name',)

admin.site.register(Card, CardAdmin)
admin.site.register(Set)
admin.site.register(Rarity)
admin.site.register(UserCard, UserCardAdmin)
admin.site.register(CardType)
admin.site.register(Keyword)
