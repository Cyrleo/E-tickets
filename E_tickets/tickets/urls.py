# from django.urls import path
# from .views import (
#     OrganisationListCreateView,
#     OrganisationDetailView,
#     EventListCreateView,
#     EventDetailBySlugView,
#     TicketPurchaseListCreateView,
#     TicketPurchaseDetailView,
#     NewsLetterListCreateView,
#     NewsLetterDetailView,
# )
#
# urlpatterns = [
#     # Organisation URLs
#     path('api/organisations/', OrganisationListCreateView.as_view(), name='organisation-list'),
#     path('organisations/<slug:slug>/', OrganisationDetailView.as_view(), name='organisation-detail'),
#
#     # Event URLs
#     path('events/', EventListCreateView.as_view(), name='event-list'),
#     path('events/<slug:slug>/', EventDetailBySlugView.as_view(), name='event-detail'),
#
#     # Ticket Purchase URLs
#     path('ticket-purchases/', TicketPurchaseListCreateView.as_view(), name='ticketpurchase-list'),
#     path('ticket-purchases/<int:pk>/', TicketPurchaseDetailView.as_view(), name='ticketpurchase-detail'),
#
#     # Newsletter URLs
#     path('newsletters/', NewsLetterListCreateView.as_view(), name='newsletter-list'),
#     path('newsletters/<int:pk>/', NewsLetterDetailView.as_view(), name='newsletter-detail'),
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrganisationViewSet, EventViewSet, TicketPurchaseViewSet, NewsLetterViewSet



router = DefaultRouter()
router.register(r'organisations', OrganisationViewSet, basename='organisation')
router.register(r'organisations/(?P<organisation_slug>[\w-]+)/events', EventViewSet, basename='organisation-events')
router.register(r'events', EventViewSet, basename='event')
router.register(r'ticket-purchases', TicketPurchaseViewSet, basename='ticketpurchase')
router.register(r'newsletters', NewsLetterViewSet, basename='newsletter')


urlpatterns = router.urls