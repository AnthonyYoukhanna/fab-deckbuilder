from django.db import models
from django.conf import settings

# -----------------------------
# Lookup Models
# -----------------------------

class CardType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class CardSubType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Keyword(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class FunctionalKeyword(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Set(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class Rarity(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# -----------------------------
# Core Models
# -----------------------------

class Card(models.Model):
    unique_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    type_text = models.CharField(max_length=200, null=True, blank=True)
    played_horizontally = models.BooleanField(default=False)

    cost = models.CharField(max_length=50, null=True, blank=True)
    pitch = models.IntegerField(choices=[(3, "Blue (3)"), (2, "Yellow (2)"), (1, "Red (1)")], null=True, blank=True)
    power = models.CharField(max_length=10, blank=True, null=True)
    defense = models.CharField(max_length=10, blank=True, null=True)
    health = models.CharField(max_length=10, blank=True, null=True)
    intelligence = models.CharField(max_length=10, blank=True, null=True)
    arcane = models.CharField(max_length=10, blank=True, null=True)

    is_token = models.BooleanField(default=False)
    is_starter = models.BooleanField(default=False)

    types = models.ManyToManyField(CardType, related_name='cards', blank=True)
    subtypes = models.ManyToManyField(CardSubType, blank=True)
    keywords = models.ManyToManyField(Keyword, blank=True)
    functional_keywords = models.ManyToManyField(FunctionalKeyword, blank=True)
    variations = models.ManyToManyField("self", symmetrical=False, blank=True)

    blitz_legal = models.BooleanField(default=True)
    cc_legal = models.BooleanField(default=True)
    commoner_legal = models.BooleanField(default=False)
    ll_legal = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class UserCard(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

# -----------------------------
# Card Printing / Version Info
# -----------------------------

class CardPrinting(models.Model):
    FOIL_CHOICES = [
        ('S', 'Standard'),
        ('R', 'Rainbow Foil'),
        ('C', 'Cold Foil'),
        ('G', 'Gold Foil')
    ]
    unique_id = models.CharField(max_length=100, unique=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='printings')
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    edition = models.CharField(max_length=10, null=True, blank=True)
    foiling = models.CharField(max_length=10, null=True, blank=True)
    rarity = models.ForeignKey(Rarity, on_delete=models.SET_NULL, null=True, blank=True)
    art_variation = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.URLField()
    tcgplayer_url = models.URLField(blank=True, null=True)
    artists = models.JSONField(default=list, blank=True)
    card_number = models.CharField(max_length=20, null=True, blank=True)
    flavour_text = models.CharField(max_length=200,blank=True,null=True)

    class Meta:
        unique_together = ('unique_id',)

    def __str__(self):
        return f"{self.card.name} ({self.set.name})"
