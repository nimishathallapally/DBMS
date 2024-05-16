from django.urls import path, include, re_path
from . import views


urlpatterns = [
    path('', views.events,name='Home-Page'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('events/add/', views.add_event,name='add_event'),
    re_path('events/fav/(?P<eventid>[0-9]+)/$',views.fav_event),
    re_path('events/unfav/(?P<eventid>[0-9]+)/$',views.unfav_event),
    re_path('events/delete/(?P<eventid>[0-9]+)/$',views.delete_event),
    path('events/listvenue/', views.list_venue, name='listvenue'),
    re_path('events/(?P<datestr>[0-9a-zA-Z]+)/(?P<selector>[0-9a-zA-Z]+)/$', views.events),
    re_path('events/(?P<datestr>[0-9a-zA-Z]+)/$', views.events),
    path('events/', views.events),
    path('logout/', views.logout_view, name='logout'),
]