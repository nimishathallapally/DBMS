from django.contrib.auth.models import User
from django.db import models



class Club(models.Model):
    name = models.CharField(unique=True, max_length=225)  # Field name made lowercase.
    dept = models.ForeignKey('Department', models.DO_NOTHING)  # Field name made lowercase.
    head_email = models.ForeignKey(User, models.DO_NOTHING,null=True)  # Field name made lowercase.



class Department(models.Model):
    head_email = models.ForeignKey(User, models.DO_NOTHING,null=True)  # Field name made lowercase.
    name = models.CharField(max_length=225)  # Field name made lowercase.



class Event(models.Model):
    # django has id for every model automatically so no need for specifying id
    # id = models.AutoField(db_column='Event_ID', primary_key=True)
    name = models.CharField(max_length=225)  # Field name made lowercase.
    description = models.TextField(blank=True, null=True)  # Field name made lowercase.
    event_creation_date_time = models.DateTimeField(blank=True, null=True)  # Field name made lowercase.
    event_start_date_time = models.DateTimeField()  # Field name made lowercase.
    event_end_date_time = models.DateTimeField()  # Field name made lowercase.
    club = models.ForeignKey(Club, models.DO_NOTHING, blank=True, null=True)  # Field name made lowercase.
    venue = models.ForeignKey('Venue', models.DO_NOTHING, blank=True, null=True)  # Field name made lowercase.
    dept = models.ForeignKey(Department, models.DO_NOTHING, blank=True, null=True)  # Field name made lowercase.
    user = models.ForeignKey(User, models.DO_NOTHING,null=True)  # Field name made lowercase.



class Favorites(models.Model):
    event = models.ForeignKey(Event, models.DO_NOTHING, related_name='fav', blank=True, null=True)  # Field name made lowercase.
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)  # Field name made lowercase.



class Venue(models.Model):
    building_name = models.CharField(max_length=225, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(max_length=225, blank=True, null=True)  # Field name made lowercase.

    #def __str__(self):
    #    return f"{self.building_name}:{self.location}"
