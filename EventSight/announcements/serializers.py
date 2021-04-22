from django.db.models import fields
from rest_framework import serializers
from .models import Student, Club, member_request, Event, Comment
from django import forms

# these are serializers


class student_login_serializer(forms.Form):
    student_id = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'student_id'}))
    password = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Password'}))
    fields = ['student_id', 'password']


class student_serializer(serializers.ModelSerializer):
    # copy fields from models.py
    class Meta:
        model = Student
        fields = '__all__'


class student_serializer_without_password(serializers.ModelSerializer):
    # copy fields from models.py
    class Meta:
        model = Student
        fields = ("student_id", "first_name", "last_name", "email", "branch")


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


class comment_serializer_with_student(serializers.ModelSerializer):
    # copy fields from models.py
    # comments = comment_serializer(read_only=True, many=True)
    student = student_serializer_without_password(read_only=True)
    class Meta:
        model = Comment
        # fields = ("student_id", "first_name", "last_name", "email", "branch")
        fields = '__all__'


class create_event_serializer(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'name'}))
    description = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'description'}))
    details = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'details'}))
    date_time = forms.DateTimeField(widget=forms.TextInput(
        attrs={'placeholder': 'date_time'}))
    open_to_all = forms.BooleanField(widget=forms.TextInput(
        attrs={'placeholder': 'open_to_all'}))
    image_url = forms.URLField(widget=forms.TextInput(
        attrs={'placeholder': 'image_url'}))
    student_id = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'student_id'}))
    fields = ['title', 'description', 'details',
              'date_time', 'open_to_all', 'image_url', 'student_id']


class universal_serializer(forms.Form):
    student_id = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'student_id'}))
    fields = ['student_id']
