from rest_framework.permissions import BasePermission
from .models import Club, Event

# https://stackoverflow.com/questions/38718454/django-rest-framework-owner-permissions
class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            if Club.objects.get(name=request.query_params.get('organizer')) == Club.objects.get(admin=request.user):
                return True
            return False
        except:
            return False


# class EventAdminPermission(BasePermission):
#     def has_permission(self, request, view):
#         print(self)
#         print(request)
#         print(view)
#         try:
#             # if Event.objects.get(pk=request.data['event_id']).organizer == Club.objects.get(admin=request.user):
#             if Event.objects.get(pk=self.request.query_params.get('event_id')).organizer == Club.objects.get(admin=request.user):
#                 return True
#             return False
#         except:
#             return False


class EventAdminPermission(BasePermission):
    

    def has_object_permission(self, request, view, obj):
        # print("HELLO, WORLD")
        print(obj.organizer.admin)
        print(request.user)
        return obj.organizer.admin == request.user
