from django.contrib import admin
from .models import Student, Club, Token, member_request, Event, Comment

# Register your models here.
admin.site.register(Student)
admin.site.register(Club)
admin.site.register(member_request)
admin.site.register(Event)
admin.site.register(Comment)
admin.site.register(Token)
