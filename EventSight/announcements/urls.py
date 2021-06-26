from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

router = DefaultRouter()

router.register('club-display', ClubDisplay, basename='club-display')
router.register('create-event', CreateEvent, basename='create-event')
router.register('display-comments', DisplayComments,
                basename='display-comments')
# router.register('retrieve-update-destroy-event',
#                 RetrieveUpdateDestroyEvent.as_view(), basename='retrieve-update-destroy-event')


urlpatterns = [
    path('', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('router/', include(router.urls)),
    path('register/', RegisterView.as_view()),
    path('refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verifytoken/', TokenVerifyView.as_view(), name='token_verify'),
    path('event-display/', EventDisplay.as_view()),
    path('interested-events-display/', InterestedEventsDisplay.as_view()),
    path('participated-events-display/', ParticipatedEventsDisplay.as_view()),
    path('retrieve-update-destroy-event/', RetrieveUpdateDestroyEvent.as_view()),
    path('retrieve-update-destroy-event/<int:pk>/', RetrieveUpdateDestroyEvent.as_view()),
    path('event-register/', AddParticipation.as_view()),
    path('event-interested/', AddInterested.as_view()),

    path('all-participants/', AllParticipants.as_view()),
    path('all-interested/', AllInterested.as_view()),
    path('get-events-via-club/', GetEventsViaClub.as_view()),
    path('clubs-not-following/', ClubsNotFollowing.as_view()),
    path('club-follow/', ClubFollow.as_view()),
    path('clubs-following/', ClubsFollowing.as_view()),
    path('club-unfollow/', ClubUnfollow.as_view()),
    path('member-request/', CreateMemberRequest.as_view()),
    path('non-member-clubs/', NonMemberClubs.as_view()),
    path('member-request-verify/', MemberRequestValidation.as_view()),
    path('get-members-requested/', GetMembersRequested.as_view()),
    path('remove-member/', RemoveMember.as_view()),
    path('member-request_check/', MemberRequestCheck.as_view()),
    # path('fetch_club/', fetch_club), # covered in ClubDisplay
    path('create-comment/', CreateComment.as_view()),
    # path('interested_participated_events/', interested_participated_events),
    # path('get_event_via_id/', get_event_via_id), # covered in event display
    path('remove-interest-participation/', RemoveInterested.as_view()),

    path('remove-interested/', RemoveInterested.as_view()),
    path('remove-participation/', RemoveParticipation.as_view()),
    # path('display-comments/', DisplayComments.as_view()),
    # path('delete_event/', delete_event), # covered in createEvent
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
