from django.db import models


class Student(models.Model):
    student_id = models.CharField(max_length=8, primary_key=True)
    password = models.CharField(max_length=1024)
    email = models.EmailField(max_length=1024)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    branch = models.CharField(max_length=64)


class Club(models.Model):

    # club will have an admin, and if we delete admin then it would do nothing
    name = models.CharField(max_length=128, primary_key=True)
    admin = models.ForeignKey(
        Student, on_delete=models.DO_NOTHING, default=None, related_name="club_admin")
    description = models.CharField(max_length=2048)
    followers = models.ManyToManyField(
        Student, blank=True, related_name="follow_list")
    members = models.ManyToManyField(
        Student, blank=True, related_name="member_list")
    image_url = models.URLField()

    def __str__(self):
        return f"{self.name}, administered by: {self.admin}"


class member_request(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, default=None)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, default=None)
    date_time = models.DateTimeField(auto_now_add=True)


class Event(models.Model):

    # if organizers are deleted, then Event would also be deleted
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    details = models.CharField(max_length=2048)
    date_time = models.DateTimeField()
    organizer = models.ForeignKey(
        Club, on_delete=models.CASCADE, related_name="event_organizers")
    interested = models.ManyToManyField(
        Student, blank=True, related_name="interested_events")
    participants = models.ManyToManyField(
        Student, blank=True, related_name="participated_events")
    open_to_all = models.BooleanField()
    image_url = models.URLField()


class Comment(models.Model):

    comment_text = models.CharField(max_length=2048)
    date_time = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, default=None)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=None)


class Token(models.Model):

    student_id = models.CharField(max_length=8, primary_key=True)
    token = models.CharField(max_length=32)

class IMAGES(models.Model):
    name = models.CharField(max_length=128, primary_key=True)
    photo = models.ImageField(upload_to='uploads/')
