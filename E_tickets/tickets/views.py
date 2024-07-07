from django.shortcuts import render , get_object_or_404 , redirect
from django.http import HttpResponse , JsonResponse
from tickets.models import Event , TicketPurchase , Organisation , NewsLetter
from tickets.forms import  TicketPurchaseForm , EventForm , ContactUsForm
from django.core.mail import send_mail ,  EmailMessage , EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.core.files.base import ContentFile
from io import BytesIO
from reportlab.pdfgen import canvas
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.graphics.barcode import code128
from django.db.models import Q
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.urls import reverse
from django.views import View
from django.core import serializers
import pyqrcode
from pyqrcode import QRCode


def index(request):
    events = Event.objects.all()
    return render(request  ,  'tickets/index.html' ,{'events':events})

def event_detail(request , event_id ):
    event = get_object_or_404( Event , pk=event_id)
    formatted_date = event.date.strftime("%A %d %B %Y ")
    formatted_time = event.time.strftime(" à %Hh%M ")

    return render(request , 'tickets/event_detail.html' , {'event' : event , 'formatted_date' : formatted_date , 'formatted_time': formatted_time})

def event_organisation_events(request ,event_id , organisation_name):
    organisation = get_object_or_404(Organisation , name = organisation_name)
    events = Event.objects.filter(organisation=organisation)
    current_event = get_object_or_404(Event , id = event_id)
    return render(request , 'tickets/event_organisation_event.html' , {'organisation': organisation, 'events': events , 'current_event': current_event })

def purchase_ticket(request, event_id):
    event = Event.objects.get(id=event_id)
    organisation = event.organisation
    form = TicketPurchaseForm(event=event)
    if request.method == 'POST':
        form = TicketPurchaseForm(request.POST, event=event)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if event.available_tickets >= quantity:
                event.available_tickets -= quantity
                event.save()
                name=form.cleaned_data["name"]

                email = form.cleaned_data['email']
                ticket_purchase = TicketPurchase.objects.create(event=event, email=email, quantity=quantity)

                pdf = generate_ticket_pdf(event.id, quantity , name)

                send_ticket_email(email, pdf, quantity)
                form = TicketPurchaseForm(event=event)
                return render(request , 'tickets/tikets_purchased.html')


    form = TicketPurchaseForm(event=event)

    context = {
        'event': event,
        'form': form,
    }
    return render(request, 'tickets/purchase_ticket.html', context)

def generate_ticket_pdf(event_id, quantity , name):

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

        x = 470
        x = 470 - 30
        barcode_value = f"{name} ticket"
        url = pyqrcode.create(barcode_value)

        
        # barcode = code128.Code128(barcode_value, barWidth=0.7, barHeight=20, row=10)
        # barcode.drawOn(p, y, x )




        # Generate QR code

        canvas.Canvas(buffer, pagesize=(10, height))
        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer

def send_ticket_email(email, pdf , quantity):
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





def organisation_events(request, organisation_name):
    if not request.user.is_authenticated:
        return render(request, 'tickets/organisation_events.html', {'message': "Vous n'êtes pas authentifié. veuillez vous authentifier avant de vous dirigez vers cette page "}  )

    if request.user.username == organisation_name:
        try:
            organisation = Organisation.objects.get(name=organisation_name)
            events = Event.objects.filter(organisation=organisation)
        except Organisation.DoesNotExist:
            organisation = None
            events = []

        return render(request, 'tickets/organisation_events.html', {'organisation': organisation, 'events': events})
    else:
        return render(request, 'tickets/organisation_events.html', {'message': "Accès non autorisé à cette organisation."} , )



# Create your views here.

def create_event(request , organisation_name):
        if request.method == 'POST':
            form = EventForm(request.POST , request.FILES)
            if not request.user.is_authenticated:
                return render(request, 'tickets/organisation_event_detail.html', {
                    'message': "Vous n'êtes pas authentifié. veuillez vous  authentifier avant de vous dirigez vers cette page  "}, )

            if form.is_valid():
                event = form.save(commit=False)
                event.organisation = Organisation.objects.get(name = organisation_name)
                event.save()
                new_letter_mail(event.id)
                return redirect('organisation' , organisation_name)
        else:
            form = EventForm()

        return render(request, 'tickets/add_event.html', {'form': form})


def update_event(request, organisation_name, event_id):
    if not request.user.is_authenticated:
        return render(request, 'tickets/organisation_event_detail.html', {'message': "Vous n'êtes pas authentifié. veuillez vous  authentifier avant de vous dirigez vers cette page  "}, )
    organisation = get_object_or_404(Organisation , name=organisation_name)
    event = get_object_or_404(Event, id=event_id, organisation = organisation)


    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event )
        if form.is_valid():
            event = form.save()
            event.save()
            return redirect('event_detail', organisation_name=organisation.name, event_id=event.id)
    else:
        form = EventForm(instance=event)

    return render(request, 'tickets/organisation_event_update.html', {'form': form , 'event':event})

def delete_event(request, organisation_name, event_id):
    if not request.user.is_authenticated:
        return render(request, 'tickets/organisation_event_detail.html', {'message': "Vous n'êtes pas authentifié. veuillez vous  authentifier avant de vous dirigez vers cette page  "}, )
    organisation = get_object_or_404(Organisation , name=organisation_name)
    event = get_object_or_404(Event, id=event_id , organisation = organisation)

    if request.method == 'POST':
        event.delete()
    return render(request , 'tickets/organisation_event_delete.html' , {'organisation_name' : organisation_name , 'event' : event })


"""
def search_event(request):
  query = request.GET.get('q')

if query:

      events = Event.objects.filter(
          Q(name__icontains=query) | Q(organisation__name__icontains=query)
      )
  else:
      events = Event.objects.all()


  context = {'events': events}
  return render(request, 'tickets/search_event.html', context)
  """


def search_event_ajax(request):
    query = request.GET.get('query')

    if query:
        #print(query)
        if query == "":
            events = Event.objects.all()
        else:
            events = Event.objects.filter(
                Q(name__icontains=query) | Q(organisation__name__icontains=query)
            )
            print(events)
            results = [
                {
                    'id': event.id,
                    'name': event.name,
                    'organisation': event.organisation,
                    'price': event.price,
                    'image': event.image,
                }
                for event in events
            ]

        results = serializers.serialize('json', events)
        return JsonResponse({'results': results})
    return HttpResponse("Evenement non trouvé !!! ")






def new_letter_mail(event_id):
    event = Event.objects.get(id=event_id)
    subject = f'Un nouvel événement vient d\'être ajouté : {event.name}'
    event_url = reverse('event-detail', args=[event_id])
    event_url = settings.BASE_URL + event_url
    message_html = mark_safe(
        f"{event.name} : {event.description}. Les détails sont disponibles <a href='{event_url}'>ici</a>.")
    message_plain = f"{event.name} : {event.description}. Les détails sont disponibles ici: {event_url}"

    from_email = settings.EMAIL_HOST_USER
    news_mails = NewsLetter.objects.values_list('email', flat=True)

    email_subject = escape(subject)
    email_message = EmailMultiAlternatives(
        email_subject,
        message_plain,
        from_email,
        news_mails
    )
    email_message.attach_alternative(message_html, "text/html")

    email_message.send()


def news(request):
    email = request.POST.get("email")
    news = NewsLetter.objects.create(email=email)
    subject = 'Votre abonnement a notre newsletter '
    message = 'Vous venez de vous abonnez a la news letter de E-tickets. Vous recevrez a partir de mantenant un mail a l\'ajout de nouveaus évènements interressant 😊 😊  '
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    email_message = EmailMessage(subject, message, from_email, recipient_list)
    email_message.send()

    return render(request , 'tickets/news.html')

def organisation_event_detail(request, organisation_name, event_id):
    if not request.user.is_authenticated:
        return render(request, 'tickets/organisation_event_detail.html', {'message': "Vous n'êtes pas authentifié. veuillez vous  authentifier avant de vous dirigez vers cette page  "}, )

    organisation = get_object_or_404(Organisation, name=organisation_name)
    event = get_object_or_404(Event, id=event_id, organisation=organisation )
    formatted_date = event.date.strftime("%A %d %B %Y ")
    formatted_time = event.time.strftime(" à %Hh%M ")

    return render(request, 'tickets/organisation_event_detail.html',{'event': event, 'organisation': organisation , 'formatted_date' : formatted_date , 'formatted_time': formatted_time})

def contact(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            send_mail(
                subject=f'Message from {form.cleaned_data["name"] or "anonyme"} ',
                message=form.cleaned_data['message'] + f"   Contactable à l adrresse {form.cleaned_data['email'] } ",
                from_email=form.cleaned_data['email'],
                recipient_list=[settings.EMAIL_HOST_USER],
            )
            return HttpResponse('Votre Méssage a bien été envoyé ! un admin du site vous fera bientôt un retour ')
        form = ContactUsForm()
    else:
        form = ContactUsForm()
    return render(request,'tickets/contact.html',{'form': form})

    return render(request, 'tickets/organisation_events_detail.html',{'message': "Accès non autorisé à cette organisation."})











from django.shortcuts import render

def pagePropos (request):
      return render( request, 'tickets/propos.html', locals() ) 

