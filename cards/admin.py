from django.contrib import admin
from .models import Card, Set, Rarity, UserCard
# Register your models here.

class UserCardAdmin(admin.ModelAdmin):
    list_display = ('user', 'card', 'quantity')
    list_filter = ('user', 'card')
    search_fields = ('user__username', 'card__name')


admin.site.register(Card)
admin.site.register(Set)
admin.site.register(Rarity)
admin.site.register(UserCard, UserCardAdmin)
