# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthorisedUser(models.Model):
    email = models.CharField(db_column='Email', primary_key=True, max_length=225)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=50)  # Field name made lowercase.
    club_name = models.CharField(db_column='Club_Name', max_length=225, blank=True, null=True)  # Field name made lowercase.
    dept = models.ForeignKey('Department', models.DO_NOTHING, db_column='Dept_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'authorised_user'


class Club(models.Model):
    club_name = models.CharField(db_column='Club_Name', primary_key=True, max_length=225)  # Field name made lowercase.
    dept = models.ForeignKey('Department', models.DO_NOTHING, db_column='Dept_ID')  # Field name made lowercase.
    club_head_email = models.CharField(db_column='Club_Head_Email', max_length=225)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'club'


class Department(models.Model):
    dept_id = models.IntegerField(db_column='Dept_ID', primary_key=True)  # Field name made lowercase.
    dept_head_email = models.CharField(db_column='Dept_Head_Email', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dept_name = models.CharField(db_column='Dept_Name', max_length=225)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'department'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Event(models.Model):
    event_id = models.AutoField(db_column='Event_ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=225)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    event_creation_date_time = models.DateTimeField(db_column='Event_Creation_Date_Time', blank=True, null=True)  # Field name made lowercase.
    event_start_date_time = models.DateTimeField(db_column='Event_Start_Date_Time')  # Field name made lowercase.
    event_end_date_time = models.DateTimeField(db_column='Event_End_Date_Time')  # Field name made lowercase.
    club_name = models.ForeignKey(Club, models.DO_NOTHING, db_column='Club_Name', blank=True, null=True)  # Field name made lowercase.
    venue = models.ForeignKey('Venue', models.DO_NOTHING, db_column='Venue_ID', blank=True, null=True)  # Field name made lowercase.
    dept = models.ForeignKey(Department, models.DO_NOTHING, db_column='Dept_ID', blank=True, null=True)  # Field name made lowercase.
    auth_email = models.ForeignKey(AuthorisedUser, models.DO_NOTHING, db_column='Auth_Email')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'event'


class Favorites(models.Model):
    event = models.ForeignKey(Event, models.DO_NOTHING, db_column='Event_ID', blank=True, null=True)  # Field name made lowercase.
    user_email = models.ForeignKey('User', models.DO_NOTHING, db_column='User_Email', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'favorites'


class User(models.Model):
    email = models.CharField(db_column='Email', primary_key=True, max_length=225)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user'


class Venue(models.Model):
    venue_id = models.IntegerField(db_column='Venue_ID', primary_key=True)  # Field name made lowercase.
    building_name = models.CharField(db_column='Building_Name', max_length=225, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=225, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'venue'
