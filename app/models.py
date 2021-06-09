from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    users = models.ManyToManyField(User, through='RoomToUser', through_fields=('room', 'user'))
    image = models.ImageField(upload_to='images', blank=True, null=True)
    is_open = models.BooleanField(default=True)
    is_drawing = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    num_of_circles = models.IntegerField(default=0)
    text = models.TextField(default='Hello World')


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
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    index = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.index is None:
            self.room.num_of_circles += 1
            self.index = self.room.num_of_circles
            self.room.save()
        return super().save(*args, **kwargs)
