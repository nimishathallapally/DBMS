from django.urls import path, include, re_path
from . import views


urlpatterns = [
    path('', views.events,name='Home-Page'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('events/add/', views.add_event,name='addevent'),
    path('events/listvenue/', views.list_venue, name='listvenue'),
    re_path('events/(?P<datestr>[0-9a-zA-Z]+)/(?P<selector>[0-9a-zA-Z]+)/$', views.events),
    re_path('events/(?P<datestr>[0-9a-zA-Z]+)/$', views.events),
    path('events/', views.events),
    path('events/add/', views.add_event, name='add_event'),
    path('logout/', views.logout_view, name='logout'),
]