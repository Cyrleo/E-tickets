from rest_framework import serializers
from .models import Organisation, Event, TicketPurchase, NewsLetter




class OrganisationSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='organisation-detail', format='html', lookup_field='slug')
    class Meta:
        model = Organisation
        fields = ['id', 'name', 'url', 'slug']  # Ajoute d'autres champs si nécessaire


class EventSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='event-detail', format='html', lookup_field='slug')
    organisation = OrganisationSerializer(read_only=True, many=False)
    class Meta:
        model = Event
        fields = ['id', 'name', 'slug', 'url', 'organisation', 'price', 'available_tickets', 'public', 'type', 'description', 'date', 'time', 'image']  # Ajoute d'autres champs si nécessaire

class OrganisationDetailSerializer(serializers.ModelSerializer):
    events = EventSerializer(read_only=True, many=False)
    class Meta:
        model = Organisation
        fields = ['id', 'name', 'url', 'events']  # Ajoute d'autres champs si nécessaire


class TicketPurchaseSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='ticketpurchase-detail', format='html', lookup_field='pk')

    class Meta:
        model = TicketPurchase
        fields = ['id', 'event', 'quantity', 'url', 'name', 'email', 'pdf']  # Ajoute d'autres champs si nécessaire

class NewsLetterSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='newsletter-detail', format='html', lookup_field='pk')

    class Meta:
        model = NewsLetter
        fields = ['id', 'email', 'url']  # Ajoute d'autres champs si nécessaire