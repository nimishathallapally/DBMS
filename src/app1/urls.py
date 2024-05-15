from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.events,name='Home-Page'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('events/add/', views.add_event),
    path('events/', views.events),
]