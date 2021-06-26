from django.core import files
from rest_framework.serializers import ModelSerializer
from .models import Comment, Event, User, Club, member_request


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']


class UserSerializer2(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class ClubSerializer(ModelSerializer):
    class Meta:
        model = Club
        fields = '__all__'


class MemberRequestSerializer(ModelSerializer):
    User = UserSerializer2(read_only=True)
    class Meta:
        model = member_request
        # fields = ['id', 'date_time', 'student', 'club']
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    User = UserSerializer2(many=True, read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'
