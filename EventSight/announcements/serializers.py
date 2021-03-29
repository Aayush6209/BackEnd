from django.db.models import fields
from rest_framework import serializers
from .models import Student, Club, member_request, Event, Comment
from django import forms

# these are serializers


class student_login_serializer(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Password'}))
    fields = ['username', 'password']


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
