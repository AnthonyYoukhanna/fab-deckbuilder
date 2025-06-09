from django.db import models
from django.conf import settings

# Create your models here.

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
class Set(models.Model):
    name = models.CharField(max_length=100)
    release_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Rarity(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class CardTypes(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Card(models.Model):

    PITCH_CHOICES = [
        (1, "Blue (1)"),
        (2, "Yellow (2)"),
        (3, "Red (3)")
    ]
    FOIL_CHOICES = [
        ('NF', 'No Foil'),
        ('RF', 'Rainbow Foil'),
        ('CF', 'Cold Foil')
    ]
    pitch = models.IntegerField(choices=PITCH_CHOICES, null=True, blank=True)
    foil = models.CharField(choices=FOIL_CHOICES, max_length=2, default='NF')

    name = models.CharField(max_length=200) #name of card
    set =  models.ForeignKey(Set, on_delete=models.CASCADE)
    rarity = models.ForeignKey(Rarity, on_delete=models.SET_NULL, null=True) #   rarity
    types = models.ManyToManyField(CardType, related_name='cards')
    #subtypes = models.ManyToManyField(CardSubType, blank=True)
    keywords = models.ManyToManyField(Keyword, blank=True)
    cost = models.CharField(max_length=50, null=True, blank=True)   #   cost
    #pitch = models.IntegerField(null=True, blank=True)#   pitch
    description = models.TextField(null=True, blank=True)   #   description

    def __str__(self):
        return self.name
    

class UserCard(models.Model):
    user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    quantity =  models.PositiveIntegerField(default=1)