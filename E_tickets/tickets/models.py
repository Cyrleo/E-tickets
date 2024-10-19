from datetime import *

from django.utils.text import slugify
from safedelete import SOFT_DELETE_CASCADE, SOFT_DELETE
from safedelete.models import SafeDeleteModel
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from account.models import User


# class SafeDeleteModel(SafeDeleteModel):
#     inserted_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         related_name='%(class)s_inserted_records',
#         # Utilisation de %(class)s pour avoir un related_name unique par modèle
#         on_delete=models.SET_NULL,
#         null=True
#     )
#     updated_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         related_name='%(class)s_updated_records',
#         # Utilisation de %(class)s pour avoir un related_name unique par modèle
#         on_delete=models.SET_NULL,
#         null=True
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
# 
#     class Meta:
#         abstract = True


class Organisation(SafeDeleteModel):
    slug = models.SlugField(unique=True, null=True, blank=True)
    _safedelete_policy = SOFT_DELETE  # Politique de suppression logique
    name = models.CharField(max_length=100, unique=True)
    users = models.ManyToManyField(User, related_name='organisations', blank=True)

    inserted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s_inserted_records',
        on_delete=models.SET_NULL,
        null=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s_updated_records',
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, keep_deleted=False, **kwargs):
        if (not self.slug or self.slug == '') and self.name:
            self.slug = slugify(self.name)
        super(Organisation, self).save(**kwargs)


    def __str__(self):
        return f'{self.name}'


class Event(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    name = models.CharField(max_length=300)
    slug = models.SlugField(null=True, blank=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True, related_name='events')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    available_tickets = models.PositiveIntegerField(default=50)
    image = models.ImageField(upload_to='events', null=True, default='events/default.jpg')
    description = models.CharField(max_length=1000, null=True)
    date = models.DateField(default=timezone.now, null=True)
    time = models.TimeField(default=timezone.now, null=True)
    inserted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s_inserted_records',
        # Utilisation de %(class)s pour avoir un related_name unique par modèle
        on_delete=models.SET_NULL,
        null=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s_updated_records',
        # Utilisation de %(class)s pour avoir un related_name unique par modèle
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, keep_deleted=False, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super(Event, self).save(**kwargs)

    class Type(models.TextChoices):
        CONCERT = 'CC'
        CONFERENCE = 'CO'
        ATTRATIONS = 'AT'
        DETENTE = 'DE'
        DIVERTISSEMENT = 'DI'
        FORMATION = 'FO'

    type = models.CharField(choices=Type.choices, max_length=8)

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


class TicketPurchase(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    email = models.EmailField()
    name = models.CharField(null=False, default='Unknown', max_length=100)
    quantity = models.PositiveIntegerField()
    pdf = models.FileField(upload_to='pdf', null=True, default='events/default.jpg')
    inserted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s_inserted_records',
        # Utilisation de %(class)s pour avoir un related_name unique par modèle
        on_delete=models.SET_NULL,
        null=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s_updated_records',
        # Utilisation de %(class)s pour avoir un related_name unique par modèle
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class NewsLetter(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    email = models.EmailField()
    inserted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s_inserted_records',
        # Utilisation de %(class)s pour avoir un related_name unique par modèle
        on_delete=models.SET_NULL,
        null=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s_updated_records',
        # Utilisation de %(class)s pour avoir un related_name unique par modèle
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.email}'
