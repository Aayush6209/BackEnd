from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .serializers import student_serializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError

# Create your views here.
"""
SuperUser
superuser@pec.edu.in
Kites@123
"""
