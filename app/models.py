from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    users = models.ManyToManyField(User, through='RoomToUser', through_fields=('room', 'user'))
    image = models.ImageField(upload_to='images', blank=True, null=True)
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class RoomToUser(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE)
    room = models.ForeignKey(Room, models.CASCADE)
    is_host = models.BooleanField()


class Circle(models.Model):
    id = models.AutoField(primary_key=True)
    x = models.IntegerField()
    y = models.IntegerField()
    r = models.IntegerField()

