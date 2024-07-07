from django.contrib import admin
from tickets.models import Organisation , Event , TicketPurchase , NewsLetter

admin.site.register(Organisation)

class EventAdmin(admin.ModelAdmin):
    list_display = [ 'name' , 'organisation']

admin.site.register(Event , EventAdmin)

class TicketAdmin(admin.ModelAdmin):
    list_display = [ 'event' , 'quantity' , 'email']

admin.site.register(TicketPurchase , TicketAdmin)

admin.site.register(NewsLetter)


