from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from rest_framework import response, serializers
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Student, Club, Event, member_request, Comment
from .serializers import student_serializer, student_login_serializer
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError


# Create your views here.
"""
user
user@pec.edu.in
user@123
"""


@api_view(['GET', 'POST'])
def register_view(request):
    if request.method == "POST":
        serializer = student_serializer(data=request.data)
        if serializer.is_valid():
            try:
                username = serializer.validated_data.get('username')
                password = serializer.validated_data.get('password')
                email = serializer.validated_data.get('email')
                first_name = serializer.validated_data.get('first_name')
                last_name = serializer.validated_data.get('last_name')
                student = Student.objects.create(
                    username=username, password=make_password(password), email=email, first_name=first_name, last_name=last_name)
                student.save()
                return Response(status=status.HTTP_201_CREATED)
            except IntegrityError:
                # username already takken or some integrity error
                return Response(serializer.data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # inappropriate fields
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # otherwise render register page
    elif request.method == "GET":
        return Response(status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
def login_view(request):
    if request.method == "POST":
        print("INSIDE POST LOGIN")
        serializer = student_login_serializer(data=request.data)
        if serializer.is_valid():
            # print("serializer is valid")
            username_pwd = serializer.data
            username = username_pwd["username"]
            password = username_pwd["password"]
            print(username)
            print(password)
            try:
                student = Student.objects.get(username=username)
                print("try success")
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            print(student.password)
            print(make_password(password))
            if check_password(password, student.password) is False:
                return Response(status=status.HTTP_403_FORBIDDEN)
            events = Event.objects.all()
            serializer = event_serializer(events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
    elif request.method == "GET":
        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def logout_view(request):
    if request.method == 'GET':
        return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def create_event(request):
    if request.method == 'GET':
        return Response(status=status.HTTP_200_OK)
    serializer = get_username(data=request.data)
    admin = serializer.data["username"]
    try:
        club = Club.objects.get(admin=admin)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        title = serializer.data["title"]
        description = serializer.data["description"]
        details = serializer.data["details"]
        date_time = serializer.data["date_time"]
        open_to_all = serializer.data["open_to_all"]
        image_url = serializer.data["image_url"]
        new_event = Event.objects.create(title=title, description=description, details=details,
                                         date_time=date_time, organizer=club, open_to_all=open_to_all, image_url=image_url)
        new_event.save()
        return Response(status=status.HTTP_201_CREATED)
    except:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def update_event(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = event_serializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = event_serializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        event.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def event_register(request):
    if request.method == 'GET':
        # return all those events where user is not registered
        events = Event.objects.exclude(Student.objects.get(
            username=request.user).participated_events)
        serializer = event_serializer(events, many=True)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        # add the student to participant list
        serializer = event_serializer(data=request.data, many=True)
        if serializer.is_valid():
            pass
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def event_interested(request):
    if request.method == 'GET':
        # return all those events where user is not interested
        pass
    elif request.method == 'POST':
        # add the event to interest list
        pass
    pass


@api_view(['GET', 'POST'])
def non_member_participation_request(request):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    pass


@api_view(['GET', 'POST'])
def non_member_participation_request_validation(request):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    pass


@api_view(['GET', 'POST'])
def club_follow(request):
    if request.method == 'GET':
        # return all those clubs where user is not following
        pass
    elif request.method == 'POST':
        # add the club to follow list
        pass
    pass


@api_view(['GET', 'POST'])
def club_unfollow(request):
    if request.method == 'GET':
        # return all those clubs where user is following
        pass
    elif request.method == 'POST':
        # remove the club to follow list
        pass
    pass


@api_view(['GET', 'POST'])
def member_request(request):
    if request.method == 'GET':
        # return all those clubs where user is not member
        pass
    elif request.method == 'POST':
        # add the member request to be validated by admin
        pass


@api_view(['GET', 'POST'])
def member_request_validation(request):
    if request.method == 'GET':
        # return all those members who requested for membership
        student = Student.objects.get(username=request.user)
        club = student.club_admin
        member_requests = member_request.objects.filter(club=club)
        students = Student.objects.filter(username=member_requests.student)
        serializer = student_serializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        # if ACCEPTED
        # add the selected member to main list
        # remove them from member_request table
        pass
    pass


@api_view(['POST'])
def create_comment(request):
    if request.method == 'POST':
        # add comment in comment table
        student = Student.objects.get(username=request.user)
        serializer = comment_serializer(data=request.data)
        if serializer.is_valid():
            try:
                comment_text = serializer.validated_data.get('comment_text')
                # event is Event object
                event = serializer.validated_data.get('event')
                new_comment = Comment.objects.create(
                    student=student, comment_text=comment_text, event=event)
                new_comment.save()
                comments = Comment.objects.all()
                serializer = comment_serializer(comments, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(serializer.data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''
{
    "password": "Kites@123",
    "username": "SuperUser"
}
'''


'''
{
    "password": "user1@123",
    "username": "19103001",
    "first_name": "Person",
    "last_name": "1",
    "email": "person1@gmail.com",
    "branch": "CSE"
}
'''

'''
{
    "title": "event1",
    "description": "this is event1",
    "details": "to be conducted at location1",
    "date_time": "2006-10-25 14:30:59",
    "open_to_all": "True",
    "image_url": "url",
    "username": "19103001"
}
'''
