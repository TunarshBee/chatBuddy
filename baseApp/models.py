from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(max_length=500, null=True)
    avatar = models.FileField(upload_to='chatBuddy_image_storage', default='avatar.svg', null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Topic(models.Model):
    
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
class Room(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null = True, blank = True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ["-updated", "-created"]
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room =models.ForeignKey(Room, on_delete=models.CASCADE)
    msgBody = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='message_like')

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.msgBody[:50]