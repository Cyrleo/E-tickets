from io import BytesIO

import pyqrcode
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import storages
from django.core.mail import EmailMessage
from reportlab.graphics.barcode import code128
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from rest_framework import viewsets, serializers, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .models import Organisation, Event, TicketPurchase, NewsLetter
from .permissions import IsOrganisationUserOrReadOnly
from .serializers import (
    OrganisationSerializer,
    EventSerializer,
    TicketPurchaseSerializer,
    NewsLetterSerializer
)


# Organisation ViewSet
class OrganisationViewSet(viewsets.ModelViewSet):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'  # Use slug for Organisation

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        # La méthode 'delete()' de SafeDeleteModel est utilisée ici pour la suppression logique
        instance.delete()


# Event ViewSet
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsOrganisationUserOrReadOnly]
    lookup_field = 'slug'  # Use slug for Event

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        organisation_slug = self.kwargs.get('organisation_slug')
        organisation = Organisation.objects.get(slug=organisation_slug)
        return organisation.events.all()  # Retourner les événements de l'organisation


# Ticket Purchase ViewSet
class TicketPurchaseViewSet(viewsets.ModelViewSet):
    queryset = TicketPurchase.objects.all()
    serializer_class = TicketPurchaseSerializer

    def perform_create(self, serializer):
        event = get_object_or_404(Event, pk=self.request.data['event'])
        quantity = self.request.data.get('quantity')
        quantity = int(quantity)
        if event.available_tickets >= quantity:
            event.available_tickets -= quantity
            event.save()
            name = self.request.data.get('name')
            email = self.request.data.get('email')
            pdf = generate_ticket_pdf(event.id, quantity, name)

            pdf_file = ContentFile(pdf.read())
            pdf_file.name = 'event_ticket.pdf'
            serializer.save(event=event, pdf=pdf_file)




        else:
            raise serializers.ValidationError("Not enough tickets available.")


def generate_ticket_pdf(event_id, quantity, name):
    event = Event.objects.get(id=event_id)
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.setTitle("Event Ticket")

    p.setFillColorRGB(0.9, 0.9, 0.9)
    p.setStrokeColorRGB(0.2, 0.2, 0.8)
    p.rect(40, 400, 520, 220, stroke=1, fill=1)
    height = 20

    if event.image:
        bg_image = ImageReader(event.image.path)
        p.drawImage(bg_image, 350, 415, width=200, height=200)
    y = 100

    p.setFillColor(colors.black)
    p.drawString(180, 660, "Event Ticket")
    p.setFont("Helvetica", 14)
    p.drawString(y, 640, f"Event: {event.name}")
    p.drawString(y, 590, f"Date: {event.date.strftime('%A, %B %d, %Y')}")
    p.drawString(y, 560, f"Time: {event.date.strftime('%I:%M %p')}")
    p.drawString(y, 530, f"organisation: {event.organisation}")

    x = 470 - 30
    barcode_value = f"{name} ticket"
    url = pyqrcode.create(barcode_value)

    barcode = code128.Code128(barcode_value, barWidth=1, barHeight=20, row=10)
    barcode.drawOn(p, y, x)

    # Generate QR code

    canvas.Canvas(buffer, pagesize=(10, height))
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer


def send_ticket_email(email, pdf, quantity):
    subject = 'Your Event Ticket'
    message = 'Thank you for purchasing tickets to the event!'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    pdf_file = ContentFile(pdf.read())
    pdf_file.name = 'event_ticket.pdf'

    email_message = EmailMessage(subject, message, from_email, recipient_list)
    email_message.attach(pdf_file.name, pdf_file.read(), 'application/pdf')
    for i in range(quantity):
        email_message.send()
    pdf_file.close()


# Newsletter ViewSet
class NewsLetterViewSet(viewsets.ModelViewSet):
    queryset = NewsLetter.objects.all()
    serializer_class = NewsLetterSerializer
