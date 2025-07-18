from django.urls import path
from. import views

urlpatterns = [
    #path Convertors
    #int: Numbers
    #str: Strings
    #path: whole urls \
    #UUID: universally unique identifiers
    #slugs: hyphen- and _underscores
    path('<int:year>/<str:month>/',views.home , name="home"),
    path('',views.home, name="home"),
    path('events', views.all_events,name="list-events"),
    path('add_venue', views.add_venue, name='add-venue'),
    path('venues', views.list_venues, name='list-venues'),
    path('show_venues/<venue_id>', views.show_venues, name='show-venues'),
    path('search_venues', views.search_venues, name='search-venues'),
    path('update_venues/<venue_id>', views.update_venues, name='update-venues'),
    path('add_event', views.add_event, name='add-event'),
    path('update_event/<event_id>', views.update_event, name='update-event'),
    path('delete_event/<event_id>', views.delete_event, name='delete-event'),
    path('delete_venue/<venue_id>', views.delete_venue, name='delete-venue'),
    path('venue_text', views.venue_text, name='venue-text'),
    path('venue_csv', views.venue_csv, name='venue-csv'),
    path('venue_pdf', views.venue_pdf, name='venue-pdf'),
    path('my_events', views.my_events, name='my_events'),
    path('search_events', views.search_events, name='search-events'),
    path('admin_approval', views.admin_approval, name='admin_approval'),
    path('venue_events/<venue_id>', views.venue_events, name='venue_events'),
    path('show_events/<event_id>', views.show_event, name='show_event'),


]
