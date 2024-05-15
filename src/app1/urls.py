from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.hi,name='Home-Page'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('event/add', views.event,name='Home-Page'),
]