from django.contrib import admin
from .models import Club, member_request, Event, Comment

# Register your models here.
admin.site.register(Club)
admin.site.register(member_request)
admin.site.register(Event)
admin.site.register(Comment)


# @admin.register(Club)
# class ClubAdmin(admin.ModelAdmin):
#     list_display = ['name', 'admin', 'description',
#                     'followers', 'members', 'club_picture']
# @admin.register(Event)
# class EventAdmin(admin.ModelAdmin):
#     list_display = ['title', 'description', 'details',
#                     'date_time', 'organizer', 'interested', 'participants', 'open_to_all', 'photo']
# @admin.register(member_request)
# class MemberRequestAdmin(admin.ModelAdmin):
#     list_display = ['User', 'club', 'date_time']
# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ['comment_text', 'date_time', 'User', 'event']
