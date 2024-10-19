from  django.urls import path
from . import views

urlpatterns = [
    path('' , views.index , name='home'),
    path('Contact-us/', views.contact, name='contact'),
    path('event/<int:event_id>/' , views.event_detail , name='event-detail'),
    path('About/', views.pagePropos, name='about'),
    path('ajax_search/' , views.search_event_ajax , name='ajax_search'),
    path('news/' , views.news , name='news'),
    path('event/<int:event_id>/purchase_ticket' , views.purchase_ticket , name='purchase_ticket'),
    path('<str:organisation_name>/' , views.organisation_events , name='organisation'),
    path('<str:organisation_name>/add_event/' , views.create_event , name='create_event'),
    path('<str:organisation_name>/<int:event_id>/update' , views.update_event , name='org_event_update'),
    path('<str:organisation_name>/<int:event_id>/delete', views.delete_event, name='org_event_delete'),
    path('<str:organisation_name>/<int:event_id>/' , views.organisation_event_detail , name='event_detail'),
    path('event/<int:event_id>/<str:organisation_name>/other_events/' , views.event_organisation_events , name='other_events'),
]
