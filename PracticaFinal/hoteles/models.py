from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Hotels(models.Model):
    name = models.TextField(default="")
    address = models.TextField(default="")
    body = models.TextField(default="")
    web = models.TextField(default="")
    category = models.TextField(default="")
    stars = models.TextField(default="")
    latitude = models.FloatField(default="")
    longitude = models.FloatField(default="")
    rate = models.IntegerField(default=0)
    def __unicode__ (self):
        return (self.name)

class Configuration(models.Model):
    user = models.ForeignKey(User)
    title = models.TextField(default="default")
    color = models.CharField(default="blue", max_length=32)
    size = models.IntegerField(default=12)
    def __unicode__ (self):
        return unicode(self.user)

class Images(models.Model):
    hotel = models.ForeignKey('Hotels')
    url = models.TextField(default="")
    def __unicode__(self):
        return unicode(self.hotel)

class Comments(models.Model):
    annotation = models.TextField(default="")
    date = models.DateField(auto_now_add=True)
    hotelCommented = models.ForeignKey('Hotels', default="")
    author = models.ForeignKey(User)
    def __unicode__(self):
        return unicode(self.author)

class Selected(models.Model):
    chosenHotel = models.ForeignKey('Hotels')
    user = models.ForeignKey(User)
    date = models.DateField(auto_now_add=True)
    def __unicode__ (self):
        return unicode(self.chosenHotel)
