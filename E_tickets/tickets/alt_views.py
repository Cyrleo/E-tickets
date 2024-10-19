from rest_framework import status, serializers, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from .models import Organisation, Event, TicketPurchase, NewsLetter
from .serializers import (
    OrganisationSerializer,
    EventSerializer,
    TicketPurchaseSerializer,
    NewsLetterSerializer
)


# Organisation Views
class OrganisationListCreateView(ListCreateAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]

class OrganisationDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    lookup_field = 'slug'  # Utilisation du champ slug pour Organisation

    permission_classes = [IsAuthenticatedOrReadOnly]

# Event Views
class EventListCreateView(ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        serializer.save()

    permission_classes = [IsAuthenticatedOrReadOnly]

class EventDetailBySlugView(generics.RetrieveUpdateDestroyAPIView):  # Changer ici pour inclure la mise à jour et la suppression
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'slug'  # Utilisation du champ slug pour Event

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Event, slug=slug)

    permission_classes = [IsAuthenticatedOrReadOnly]

# Ticket Purchase Views
class TicketPurchaseListCreateView(ListCreateAPIView):
    queryset = TicketPurchase.objects.all()
    serializer_class = TicketPurchaseSerializer

    def perform_create(self, serializer):
        event = get_object_or_404(Event, pk=self.request.data['event'])
        quantity = self.request.data.get('quantity')
        if event.available_tickets >= quantity:
            event.available_tickets -= quantity
            event.save()
            serializer.save(event=event)
        else:
            raise serializers.ValidationError("Not enough tickets available.")


class TicketPurchaseDetailView(RetrieveUpdateDestroyAPIView):
    queryset = TicketPurchase.objects.all()
    serializer_class = TicketPurchaseSerializer


# Newsletter Views
class NewsLetterListCreateView(ListCreateAPIView):
    queryset = NewsLetter.objects.all()
    serializer_class = NewsLetterSerializer


class NewsLetterDetailView(RetrieveUpdateDestroyAPIView):
    queryset = NewsLetter.objects.all()
    serializer_class = NewsLetterSerializer