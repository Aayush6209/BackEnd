from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .serializers import event_serializer, student_serializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import Student, Club, Event, member_request, Comment
from .serializers import student_serializer, student_login_serializer

# Create your views here.
"""
SuperUser
superuser@pec.edu.in
Kites@123
"""


@api_view(['GET', 'POST'])
def register_view(request):
    if request.method == "POST":
        serializer = student_serializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                student = serializer.validated_data()
                login(request, student)
                events = Event.objects.all()
                serializer = event_serializer(events, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                # username already takken
                return Response(serializer.data, status=status.HTTP_409_CONFLICT)

        # inappropriate fields
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # otherwise render register page


@api_view(['GET', 'POST'])
def login_view(request):
    if request.method == "POST":
        serializer = student_login_serializer(data=request.data)
        if serializer.is_valid():
                username_pwd = serializer.validated_data()
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
        else:
            return Response(serializer.data, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def logout_view(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)
