from django.db.models import fields
from rest_framework import serializers
from .models import Student, Club, member_request, Event, Comment

# these are serializers


class student_serializer(serializers.ModelSerializer):
    # copy fields from models.py
    class Meta:
        model = Student
        fields = '__all__'


class club_serializer(serializers.ModelSerializer):
    # copy fields from models.py
    class Meta:
        model = Club
        fields = '__all__'


class member_request_serializer(serializers.ModelSerializer):
    # copy fields from models.py
    class Meta:
        model = member_request
        fields = '__all__'


class event_serializer(serializers.ModelSerializer):
    # copy fields from models.py
    class Meta:
        model = Event
        fields = '__all__'


class comment_serializer(serializers.ModelSerializer):
    # copy fields from models.py
    class Meta:
        model = Comment
        fields = '__all__'
