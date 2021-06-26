from django.db import models
from django.contrib.auth.models import User


class Club(models.Model):

    name = models.CharField(max_length=128, primary_key=True)
    admin = models.ForeignKey(
        User, on_delete=models.PROTECT, default=None, related_name="club_admin")
    description = models.CharField(max_length=2048)
    followers = models.ManyToManyField(
        User, blank=True, related_name="follows")
    members = models.ManyToManyField(
        User, blank=True, related_name="club")
    club_picture = models.ImageField(upload_to='club_uploads/', blank=True)


class member_request(models.Model):
    User = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, default=None)
    date_time = models.DateTimeField(auto_now_add=True)


class Event(models.Model):

    # if organizers are deleted, then Event would also be deleted
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    details = models.CharField(max_length=2048)
    date_time = models.DateTimeField()
    organizer = models.ForeignKey(
        Club, on_delete=models.CASCADE)
    interested = models.ManyToManyField(
        User, blank=True, related_name="interests")
    participants = models.ManyToManyField(
        User, blank=True, related_name="event")
    open_to_all = models.BooleanField()
    photo = models.ImageField(upload_to="upload/", blank=True)


class Comment(models.Model):

    comment_text = models.CharField(max_length=2048)
    date_time = models.DateTimeField(auto_now_add=True)
    User = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=None)
