from django.contrib.auth.models import User
from .serializers import ClubSerializer, CommentSerializer, MemberRequestSerializer, UserSerializer, UserSerializer2, EventSerializer
from .models import Club, Event, member_request, Comment
from datetime import datetime
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter
from .custompermissions import AdminPermission, EventAdminPermission
from rest_framework.response import Response
from rest_framework import status

# OK
class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class Profile(ListAPIView):
    serializer_class = UserSerializer2
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.get(pk=self.request.user.pk)
    

# OK
class EventDisplay(ListAPIView):
    serializer_class = EventSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ['date_time']

    def get_queryset(self):
        user = self.request.user

        followed_club_events = Event.objects.filter(organizer__in=user.follows.all()).filter(
            open_to_all=True).filter(date_time__gt=datetime.now())

        member_club_events = Event.objects.filter(organizer__in=user.club.all()).filter(date_time__gt=datetime.now())

        # return the union
        return followed_club_events | member_club_events

# OK
class InterestedEventsDisplay(ListAPIView):
    serializer_class = EventSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ['date_time']

    def get_queryset(self):
        user = self.request.user
        interesetd_events = Event.objects.filter(
            interested=user).filter(date_time__gt=datetime.now())
        return interesetd_events

# OK
class ParticipatedEventsDisplay(ListAPIView):
    serializer_class = EventSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ['date_time']

    def get_queryset(self):
        user = self.request.user
        interesetd_events = Event.objects.filter(
            participants=user).filter(date_time__gt=datetime.now())
        return interesetd_events

# OK
class CreateEvent(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminPermission]

# OK
class RetrieveUpdateDestroyEvent(RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, EventAdminPermission]

# OK
class AddParticipation(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, pk=None, format=None):
        try:
            event = Event.objects.get(pk=request.data['event_id'])
            event.participants.add(self.request.user)
            return Response({"message": "You are successfully registered!"}, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# OK
class AddInterested(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, pk=None, format=None):
        try:
            event = Event.objects.get(pk=request.data['event_id'])
            event.interested.add(self.request.user)
            return Response({"message": "You are successfully added!"}, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# OK
class RemoveInterested(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None, format=None):
        event = Event.objects.get(pk=request.data['event_id'])
        event.interested.remove(self.request.user)
        return Response({'msg': 'Removed'}, status=status.HTTP_200_OK)

# OK
class RemoveParticipation(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None, format=None):
        event = Event.objects.get(pk=request.data['event_id'])
        event.participants.remove(self.request.user)
        return Response({'msg': 'Removed'}, status=status.HTTP_200_OK)

# OK
class AllParticipants(ListAPIView):
    serializer_class = UserSerializer2
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            event = Event.objects.get(pk=self.request.query_params.get('event_id'))
            return event.participants.all()
        except:
            return None

# OK
class AllInterested(ListAPIView):
    serializer_class = UserSerializer2
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, EventAdminPermission]

    def get_queryset(self):
        event = Event.objects.get(pk=self.request.query_params.get('event_id'))
        return event.interested.all()

# OK
class GetEventsViaClub(ListAPIView):
    serializer_class = EventSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ['date_time']

    def get_queryset(self):
        club = Club.objects.get(pk=self.request.query_params.get('club_id'))
        student = User.objects.get(pk=self.request.user.pk)
        if club in student.club.all():
            return Event.objects.filter(organizer=club)
        return Event.objects.filter(organizer=club).filter(open_to_all=True)

# OK
class ClubDisplay(viewsets.ReadOnlyModelViewSet):
    serializer_class = ClubSerializer
    queryset = Club.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

# APPLY ClubsFollowing functionality if not working
# OK
class ClubsNotFollowing(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ClubSerializer

    def get_queryset(self):
        student = User.objects.get(pk=self.request.user.pk)
        return Club.objects.exclude(pk__in=student.follows.all())

# OK
class ClubFollow(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk=None, format=None):
        try:
            club_name = request.data['club_name']
            Club.objects.get(pk=club_name).followers.add(User.objects.get(pk=self.request.user.pk))
            return Response({"message": f"Followed {club_name}"}, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# OK
class ClubsFollowing(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ClubSerializer

    def get_queryset(self):
        student = User.objects.get(pk=self.request.user.pk)
        return Club.objects.filter(pk__in=student.follows.all())

# OK
class ClubUnfollow(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk=None, format=None):
        try:
            club_name = request.data['club_name']
            Club.objects.get(pk=club_name).followers.remove(
                User.objects.get(pk=self.request.user.pk))
            return Response({"message": f"Unfollowed {club_name}!"}, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# OK
class NonMemberClubs(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ClubSerializer

    def get_queryset(self):
        student = User.objects.get(pk=self.request.user.pk)
        return Club.objects.exclude(pk__in=student.club.all())


# OK
class CreateMemberRequest(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None, format=None):
        try:
            club_name = request.data['club_name']
            club = Club.objects.get(pk=club_name)
            if member_request.objects.filter(User=self.request.user, club=club) is not None:
                return Response({"message": f"Request for membership of {club.name} club is under process."}, status=status.HTTP_200_OK)
            new_request = member_request.objects.create(
                User=self.request.user, club=club)
            new_request.save()
            return Response({"message": f"Requested membership for {club.name}"}, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# OK
class GetMembersRequested(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminPermission]
    serializer_class = MemberRequestSerializer

    def get_queryset(self):
        admin = self.request.user
        member_requests = member_request.objects.filter(club=Club.objects.get(admin=admin))
        return member_requests


class MemberRequestValidation(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AdminPermission]

    def post(self, request, pk=None, format=None):
        student = User.objects.get(pk=request.data['student_id'])
        club = Club.objects.get(pk=request.data['club'])
        accepted = request.data['accepted']
        req = member_request.objects.filter(student=student, club=club)
        req.delete()
        if accepted:
            club.members.add(student)
            club.followers.add(student)
        return Response(status=status.HTTP_200_OK)


class RemoveMember(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None, format=None):
        student = self.request.user
        club = Club.objects.get(name=request.data['club_name'])
        club.members.remove(student)
        return Response({'message': f'Removed from {club.name}'}, status=status.HTTP_200_OK)


class MemberRequestCheck(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None, format=None):
        student = self.request.user
        club = Club.objects.get(name=request.data['name'])
        try:
            member_request_data = member_request.objects.filter(student=student, club=club)
            return Response(MemberRequestSerializer(member_request_data).data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)


class CreateComment(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None, format=None):
        try:
            comment_text = request.data['comment_text']
            event = Event.objects.get(pk=request.data['event_id'])
            new_comment = Comment.objects.create(
                student=self.request.user, comment_text=comment_text, event=event)
            new_comment.save()
            comments = Comment.objects.filter(event=event)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# class CreateComment(CreateAPIView):
#     queryset = Comment.objects.all()
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]


class DisplayComments(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['date_time']

    def get_queryset(self):
        event_id = self.request.query_params('event_id')
        return Comment.objects.filter(event__id=event_id)
