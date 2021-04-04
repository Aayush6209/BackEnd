from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from rest_framework import response, serializers
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Student, Club, Event, member_request, Comment
from .serializers import universal_serializer, student_login_serializer, student_serializer
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError


# Create your views here.
"""
user
user@gmail.com
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
        # print("INSIDE POST LOGIN")
        serializer = student_login_serializer(data=request.data)
        if serializer.is_valid():
            # # print("serializer is valid")
            username_pwd = serializer.data
            username = username_pwd["username"]
            password = username_pwd["password"]
            # print(username)
            # print(password)
            try:
                student = Student.objects.get(username=username)
                # print("try success")
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # print(student.password)
            # print(make_password(password))
            if check_password(password, student.password) is False:
                return Response(status=status.HTTP_403_FORBIDDEN)
            events = Event.objects.all()
            serializer = event_serializer(events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
    elif request.method == "GET":
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        serializer = universal_serializer(data=request.data)
        username = serializer.data['username']
        return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def create_event(request):
    try:
        serializer = universal_serializer(data=request.data)
        admin = serializer.data["username"]
        print("admin is:", admin)
    except:
        # print("1")
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    # if admin not in active_users:
    #     # print("2")
    #     # print(active_users)
    #     return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        club = Club.objects.get(admin=admin)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        try:
            events = Event.objects.filter(organizer=club)
        except:
            events = None
        serializer = event_serializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
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


@api_view(['PUT', 'DELETE'])
def update_event(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    try:
        serializer = universal_serializer(data=request.data)
        admin = serializer.data["username"]
    except:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    # if admin not in active_users:
    #     return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        club = Club.objects.get(admin=admin)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if club != event.organizer:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'PUT':
        try:
            event.title = serializer.data["title"]
            event.description = serializer.data["description"]
            event.details = serializer.data["details"]
            event.date_time = serializer.data["date_time"]
            event.open_to_all = serializer.data["open_to_all"]
            event.image_url = serializer.data["image_url"]
            event.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        event.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def event_register(request):
    if request.method == 'GET':
        # return all those events where user is not registered
        try:
            events = Event.objects.all()
            serializer = event_serializer(events, many=True)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        # add the student to participant list
        try:
            serializer = universal_serializer(data=request.data)
            event = Event.objects.get(pk=serializer.data["id"])
            student = Student.objects.get(username=serializer.data["username"])
            # if student not in active_users:
            #     return Response(status=status.HTTP_401_UNAUTHORIZED)
            if student in event.participants:
                return Response({"message": "You are already registered!"}, status=status.HTTP_200_OK)
            if event.open_to_all is True:
                event.participants.add(student)
                return Response({"message": "You are successfully registered!"}, status=status.HTTP_200_OK)
            else:
                if student in event.organizer.members:
                    event.participants.add(student)
                    return Response({"message": "You are successfully registered!"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "This event is only for members."}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def event_interested(request):
    if request.method == 'GET':
        # return all the events
        try:
            events = Event.objects.all()
            serializer = event_serializer(events, many=True)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        # add the event to interest list
        try:
            serializer = universal_serializer(data=request.data)
            event = Event.objects.get(pk=serializer.data["id"])
            student = Student.objects.get(username=serializer.data["username"])
            # if student not in active_users:
            #     return Response(status=status.HTTP_401_UNAUTHORIZED)
            if student in event.interested:
                return Response({"message": "You are already interested!"}, status=status.HTTP_200_OK)
            if event.open_to_all is True:
                event.interested.add(student)
                return Response({"message": "You are successfully added to interested list!"}, status=status.HTTP_200_OK)
            else:
                if student in event.organizer.members:
                    event.interested.add(student)
                    return Response({"message": "You are successfully added to interested list!"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "This event is only for members."}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'POST'])
# def non_member_participation_request(request):
#     if request.method == 'GET':
#         pass
#     elif request.method == 'POST':
#         pass
#     pass


# @api_view(['GET', 'POST'])
# def non_member_participation_request_validation(request):
#     if request.method == 'GET':
#         pass
#     elif request.method == 'POST':
#         pass
#     pass


@api_view(['GET', 'POST'])
def club_follow(request):
    serializer = universal_serializer(data=request.data)
    username=serializer.data['username']
    student = Student.objects.get(username=username)
    if request.method == 'GET': ---
        # return all those clubs where user is not following
        follow_list = student.follow_list.filter()
        ids = []
        for i in follow_list:
            ids.append(i.pk)
        clubs_not_in_follow_list = Club.objects.exclude(pk__in=ids)
        serializer = club_serializer(clubs_not_in_follow_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        # add the club to follow list
        # TODO primary key need to be set
        club_id = serializer.data["club_id"]
        club = Club.objects.get(pk=club_id)
        club.followers.add(student)
        return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def club_unfollow(request):
    serializer = universal_serializer(data=request.data)
    username = serializer.data['username']
    student = Student.objects.get(username=username)
    if request.method == 'GET':
        # return all those clubs where user is not following
        follow_list = student.follow_list.filter()
        ids = []
        for i in follow_list:
            ids.append(i.pk)
        clubs_not_in_follow_list = Club.objects.filter(pk__in=ids)
        serializer = club_serializer(clubs_not_in_follow_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        # add the club to follow list
        club_id = serializer.data["club_id"]
        club = Club.objects.get(pk=club_id)
        club.followers.remove(username)
        return Response(status=status.HTTP_200_OK)


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
        pass
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

# login
'''
{
    "password": "user2@123",
    "username": "19103002"
}
'''

# register
'''
{
    "password": "user2@123",
    "username": "19103002",
    "first_name": "Person",
    "last_name": "2",
    "email": "person2@gmail.com",
    "branch": "CSE"
}
'''

# logout
'''
{
    "username": "19103002",
}
'''

# create_event, update_event/pk
'''
{
    "title": "event2",
    "description": "this is event2",
    "details": "to be conducted at location2",
    "date_time": "2006-10-25 14:30:59",
    "open_to_all": "True",
    "image_url": "url",
    "username": "19103001"
}
'''

# event_register
# here id is event_id
'''
{
    "id": "2",
    "username": "19103026"
}
'''
