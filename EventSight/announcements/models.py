from django.db import models

'''
CREATE TABLE Student(
    student_id varchar(8),
    password varchar(1024),
    email varchar(1024),
    first_name varchar(64),
    last_name varchar(64),
    branch varchar(64),
    primary key (student_id)
    
);
'''
class Student(models.Model):
    student_id = models.CharField(max_length=8, primary_key=True)
    password = models.CharField(max_length=1024)
    email = models.EmailField(max_length=1024)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    branch = models.CharField(max_length=64)


'''
CREATE TABLE Club(
    name varchar(128),
    admin varchar(128), 
    description varchar(1024), 
    image_url varchar(2000),
    primary key (name),
    foreign key (admin) references Student (student_id)
    
);
'''
'''
CREATE TABLE followers(
    student_id varchar(128),
    club_id int,
    foreign key (student_id) references Student (student_id),
    foreign key (club_id) references Club (name)
    
);
'''
'''
CREATE TABLE members(
    student_id varchar(128),
    club_id int,
    foreign key (student_id) references Student (student_id),
    foreign key (club_id) references Club (name)
);
'''

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

'''
CREATE TABLE member_request(
    student varchar(128),
    club int, 
    date_time datetime, 
    foreign key (club) references Club (name),
    foreign key (student) references Student (student_id)
    
);
'''





class member_request(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, default=None)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, default=None)
    date_time = models.DateTimeField(auto_now_add=True)




'''
CREATE TABLE Event(
    event_id int,
    title varchar(128),
    description varchar(2048), 
    details varchar(2048),
    date_time datetime,
    organiser int,
    open_to_all bool,
    image_url varchar(2000),
    primary key(event_id),
    foreign key (organiser) references Club (name)
    
);
'''
'''
CREATE TABLE interested(
    student_id varchar(128),
    event_id int,
    foreign key (student_id) references Student (student_id),
    foreign key (event_id) references Event (event_id)
    
);
'''
'''
CREATE TABLE participants(
    student_id varchar(128),
    event_id int,
    foreign key (student_id) references Student (student_id),
    foreign key (event_id) references Event (event_id)
    
);
'''
'''
CREATE TABLE participation_request(
    student_id varchar(128),
    event_id int,
    date_time date,
    foreign key (student_id) references Student (student_id),
    foreign key (event_id) references Event (event_id)
    
    
);
'''


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

'''
CREATE TABLE Comment(
    comment_id int,
    comment_txt varchar(2048),
    student_id varchar(128),
    event_id int,
    date_time date,
    primary key(comment_id),
    foreign key (student_id) references Student (student_id),
    foreign key (event_id) references Event (event_id)
    
);
'''

class Comment(models.Model):

    comment_text = models.CharField(max_length=2048)
    date_time = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, default=None)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=None)


class Token(models.Model):

    student_id = models.CharField(max_length=8, primary_key=True)
    token = models.CharField(max_length=32)