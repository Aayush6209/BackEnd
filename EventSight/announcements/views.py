from os import stat
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from rest_framework import response, serializers
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Student, Club, Event, Token, member_request, Comment
from .serializers import universal_serializer, student_login_serializer, student_serializer
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError
from django.utils.crypto import get_random_string


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
                student_id = serializer.validated_data.get('student_id')
                password = serializer.validated_data.get('password')
                email = serializer.validated_data.get('email')
                first_name = serializer.validated_data.get('first_name')
                last_name = serializer.validated_data.get('last_name')
                branch = serializer.validated_data.get('branch')
                student = Student.objects.create(
                    student_id=student_id, password=make_password(password), email=email, first_name=first_name, last_name=last_name, branch=branch)
                student.save()

                events = Event.objects.all()
                serializer = event_serializer(events, many=True)
                new_token = Token.objects.create(
                    student_id=student_id, token=get_random_string(length=32))
                new_token.save()
                return Response({"events": serializer.data,
                                "student_id": new_token.student_id,
                                "token": new_token.token
                                }, status=status.HTTP_201_CREATED)
                                
            except IntegrityError:
                # student_id already takken or some integrity error
                return Response(serializer.data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # inappropriate fields
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # otherwise render register page
    elif request.method == "GET":
        return Response(status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
def login_view(request):
    if request.method == "POST":
        serializer = universal_serializer(data=request.data)
        student_id = serializer.data["student_id"]
        password = serializer.data["password"]
        role = serializer.data["role"]
        club = serializer.data["club"]
        try:
            student = Student.objects.get(student_id=student_id)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if check_password(password, student.password) is False:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if (role == "Admin"):
            club_of_admin = Club.objects.get(name=club)
            if (club_of_admin.admin != student):
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        credentials = student_serializer(student)
        new_token = Token.objects.create(
            student_id=student_id, token=get_random_string(length=32))
        new_token.save()
        return Response({"credentials": credentials.data,
                         "token": new_token.token
                         }, status=status.HTTP_200_OK)
    elif request.method == "GET":
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        serializer = universal_serializer(data=request.data)
        student_id = serializer.data['student_id']
        token_got = serializer.data['token']
        token = Token.objects.get(student_id=student_id)
        if (token.token != token_got):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        token.delete()
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def event_display(request):
    serializer = universal_serializer(data=request.data)
    student_id = serializer.data['student_id']
    token_got = serializer.data['token']
    token = Token.objects.get(student_id=student_id)
    if (token.token != token_got):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    student = Student.objects.get(student_id=student_id)
    if request.method == 'GET':
        follow_list = student.follow_list.filter()
        followed_club_events = Event.request.filter(organizer__in=follow_list)

        events_open_to_all = Event.request.filter(open_to_all=True)

        return Response(
                    {
                        "followed_club_events": event_serializer(followed_club_events, many=True).data,
                        "events_open_to_all": event_serializer(events_open_to_all, many=True).data
                    },
                    status=status.HTTP_200_OK)
    elif request.method == 'POST':
        pk=serializer.data['pk']
        return Response(event_serializer(Event.objects.get(pk=pk)).data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST'])
def create_event(request):
    try:
        serializer = universal_serializer(data=request.data)
        admin = serializer.data["student_id"]
        token_got = serializer.data['token']
        token = Token.objects.get(student_id=admin)
        if (token.token != token_got):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
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
        admin = serializer.data["student_id"]
        token_got = serializer.data['token']
        token = Token.objects.get(student_id=admin)
        if (token.token != token_got):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
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
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        # add the student to participant list
        try:
            serializer = universal_serializer(data=request.data)
            event = Event.objects.get(pk=serializer.data["id"])
            student_id = serializer.data["student_id"]
            token_got = serializer.data['token']
            token = Token.objects.get(student_id=student_id)
            if (token.token != token_got):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            student = Student.objects.get(student_id=student_id)
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
            print(events)
            serializer = event_serializer(events, many=True)
            print(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        # add the event to interest list
        try:
            serializer = universal_serializer(data=request.data)
            event = Event.objects.get(pk=serializer.data["id"])
            student_id = serializer.data["student_id"]
            token_got = serializer.data['token']
            token = Token.objects.get(student_id=student_id)
            if (token.token != token_got):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            student = Student.objects.get(student_id=student_id)
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


@api_view(['POST'])
def get_events_via_club(request):
    serializer = universal_serializer(data=request.data)
    club=serializer.data['club_id']
    return Response(
        event_serializer(club.event_organizers.filter(), many=True),
        status=status.HTTP_200_OK
    )


@api_view(['GET', 'POST'])
def club_display(request):
    serializer = universal_serializer(data=request.data)
    # student_id = serializer.data['student_id']
    # student = Student.objects.get(student_id=student_id)
    if request.method == 'GET':
        clubs = Club.objects.all()
        return Response(
                club_serializer(clubs, many=True).data,
                status=status.HTTP_200_OK
        )
    elif request.method == 'POST':
        pk = serializer.data['pk']
        return Response(
            club_serializer(Club.objects.get(pk=pk)).data,
            status=status.HTTP_200_OK
        )
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def club_follow(request):
    serializer = universal_serializer(data=request.data)
    student_id=serializer.data['student_id']

    token_got = serializer.data['token']
    token = Token.objects.get(student_id=student_id)
    if (token.token != token_got):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    student = Student.objects.get(student_id=student_id)
    if request.method == 'GET':
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
        club_name = serializer.data["name"]
        club = Club.objects.get(pk=club_name)
        club.followers.add(student)
        return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def club_unfollow(request):
    serializer = universal_serializer(data=request.data)
    student_id = serializer.data['student_id']
    token_got = serializer.data['token']
    token = Token.objects.get(student_id=student_id)
    if (token.token != token_got):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    student = Student.objects.get(student_id=student_id)
    if request.method == 'GET':
        # return all those clubs where user is following
        follow_list = student.follow_list.filter()
        ids = []
        for i in follow_list:
            ids.append(i.pk)
        clubs_not_in_follow_list = Club.objects.filter(pk__in=ids)
        serializer = club_serializer(clubs_not_in_follow_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        # remove the club from follow list
        club_name = serializer.data["name"]
        club = Club.objects.get(pk=club_name)
        club.followers.remove(student)
        return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def create_member_request(request):
    serializer = universal_serializer(data=request.data)
    student_id = serializer.data['student_id']
    token_got = serializer.data['token']
    token = Token.objects.get(student_id=student_id)
    if (token.token != token_got):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    student = Student.objects.get(student_id=student_id)
    if request.method == 'GET':
        # return all those clubs where user is not member
        member_list = student.member_list.filter()
        ids = []
        for i in member_list:
            ids.append(i.pk)
        clubs_not_in_member_list = Club.objects.exclude(pk__in=ids)
        serializer = club_serializer(clubs_not_in_member_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        # add the club to follow list
        club_name = serializer.data["name"]
        club = Club.objects.get(name=club_name)
        new_member_request = member_request.objects.create(student=student, club=club)
        new_member_request.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def member_request_validation(request):
    serializer = universal_serializer(data=request.data)
    student_id = serializer.data['student']
    token_got = serializer.data['token']
    token = Token.objects.get(student_id=student_id)
    if (token.token != token_got):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    student = Student.objects.get(student_id=student_id)
    if request.method == 'GET':
        # return all those members who requested for membership
        club = Club.objects.get(name=student.club_admin.get().name)
        member_requests = member_request.objects.filter(club=club)
        serializer = member_request_serializer(member_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        club = Club.objects.get(name=serializer.data["club"])
        print(club)
        print(student)
        accepted = serializer.data["accepted"]
        member_requested = member_request.objects.get(student=student, club=club)
        member_requested.delete()
        # if ACCEPTED
        if accepted:
            # add the selected member to main list
            club.members.add(student)
            club.followers.add(student)
        # remove them from member_request table
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def create_comment(request):
    serializer = universal_serializer(data=request.data)
    student_id = serializer.data['student_id']
    token_got = serializer.data['token']
    token = Token.objects.get(student_id=student_id)
    if (token.token != token_got):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    student = Student.objects.get(student_id=student_id)
    if request.method == 'POST':
        comment_text = serializer.data['comment_text']
        event = Event.objects.get(pk=serializer.data['event'])
        new_comment = Comment.objects.create(
            student=student, comment_text=comment_text, event=event)
        new_comment.save()
        comments = Comment.objects.filter(event=event)
        serializer = comment_serializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# token, student_id field REQUIRED in all the POST/GET methods.

# login

'''
{
    "password": "user2@123",
    "student_id": "19103002",
    "role": "Admin/Student",
    "club": "club-name"
}
'''

# register
'''
{
    "password": "user2@123",
    "student_id": "19103002",
    "first_name": "Person",
    "last_name": "2",
    "email": "person2@gmail.com",
    "branch": "CSE"
}
'''

# logout
'''
{
    "student_id": "19103002",
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
    "student_id": "19103001"
}
'''

# event_register
# here id is event_id
'''
{
    "id": "2",
    "student_id": "19103026"
}
'''

# club follow/unfollow GET
'''
{
    "student_id": "19103002"
}
'''


# club follow/unfollow POST
'''
{
    "student_id": "19103002",
    "name": "Club1"
}
'''

# member_request GET
'''
{
    "student_id": "19103026"
}
'''

# member_request POST
'''
{
    "student_id": "19103002",
    "name": "Club1"
}
'''

# member_request_validation GET
'''
{
    "student": "19103002"
}
'''

# member_request_validation POST
'''
{
    "student": "19103002",
    "club": "Club1",
    "accepted": true
}
'''

# create_comment POST
'''
{
    "comment_text": "This is comment1.",
    "student": "19103002",
    "event": "event_id"
}
'''
