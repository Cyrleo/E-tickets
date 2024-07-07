from django.db import models
from datetime import *
from django.core.validators import MinValueValidator
from django.utils import timezone

class Organisation(models.Model):
    name=models.CharField(max_length=100 , unique = True     )

    def __str__(self):
        return f'{self.name}'

class Event(models.Model):
    name = models.CharField(max_length=300)
    organisation = models.ForeignKey(Organisation , on_delete=models.CASCADE , null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2 , null = True)
    available_tickets = models.PositiveIntegerField( default= 50 )
    image = models.ImageField(upload_to='events', null=True , default='events/default.jpg')
    description = models.CharField(max_length = 1000 , null = True)
    date = models.DateField(default = timezone.now().date() , null = True )
    time = models.TimeField(default = timezone.now , null = True)

    class Type(models.TextChoices):
        CONCERT = 'CC'
        CONFERENCE = 'CO'
        ATTRATIONS = 'AT'
        DETENTE = 'DE'
        DIVERTISSEMENT = 'DI'
        FORMATION = 'FO'

    type = models.CharField(choices=Type.choices , max_length=8)


    class Public(models.TextChoices):
        ETUDIANTS = 'ET'
        PROFESSIONNEL = 'PR'
        TOUT_TYPE = 'TT'
        ENFANT = 'EF'
        ADULTE = 'AD'
        HOMME = 'HO'
        FEMME = 'FE'

    public = models.CharField(choices=Public.choices, max_length=8)
    def __str__(self):
        return f'{self.name}'

class TicketPurchase(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    email = models.EmailField()
    quantity = models.PositiveIntegerField()

class NewsLetter(models.Model):
    email = models.EmailField()
    def __str__(self):
        return f'{self.email}'