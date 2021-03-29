from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from rest_framework import response
from .serializers import event_serializer, student_serializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import Student, Club, Event, member_request, Comment
from .serializers import student_serializer, student_login_serializer

# from colorama import Fore, Style

# Create your views here.
"""
SuperUser
superuser@pec.edu.in
Kites@123
"""


@api_view(['GET', 'POST'])
def register_view(request):
    if request.method == "POST":
        print("inside post")
        serializer = student_serializer(data=request.data)
        if serializer.is_valid():
            print("serializer is valid")
            try:
                username = serializer.validated_data.get('username')
                password = serializer.validated_data.get('password')
                email = serializer.validated_data.get('email')
                first_name = serializer.validated_data.get('first_name')
                last_name = serializer.validated_data.get('last_name')
                student = Student.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                student.save()
                events = Event.objects.all()
                serializer = event_serializer(events, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                # username already takken or some integrity error
                return Response(serializer.data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # inappropriate fields
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # otherwise render register page
    elif request.method == "GET":
        users = Student.objects.all()
        serializer = student_serializer(users, many=True)
        return Response(serializer.data)


@api_view(['POST', 'GET'])
def login_view(request):
    if request.method == "POST":
        serializer = student_login_serializer(data=request.data)
        if serializer.is_valid():
            print("serializer is valid")
            username_pwd = serializer.data
            username = username_pwd["username"]
            password = username_pwd["password"]
            student = authenticate(request, username=username, password=password)
            if student is not None:
                login(request, student)
                events = Event.objects.all()
                serializer = event_serializer(events, many=True)
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.data, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
    elif request.method == "GET":
        users = Student.objects.all()
        serializer = student_serializer(users, many=True)
        return Response(serializer.data)



@api_view(['GET'])
def logout_view(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)

'''
{
    "password": "Kites@123",
    "username": "SuperUser"
}
'''


'''
{
    "password": "user2@123",
    "username": "19103002",
    "first_name": "Person",
    "last_name": "2",
    "email": "person2@gmail.com"
}
'''
