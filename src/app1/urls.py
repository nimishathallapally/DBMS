from django.urls import path, include, re_path
from . import views


urlpatterns = [
    path('', views.events,name='Home-Page'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('event/add/', views.event,name='addevent'),
    path('event/listvenue/', views.list_venue, name='listvenue'),
    re_path('events/(?P<selector>[0-9a-zA-Z]+)/$', views.events),
    path('events/', views.events),
]