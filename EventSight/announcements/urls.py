from django.urls import path

from .views import *

urlpatterns = [
    path('register/', register_view),
    path('login/', login_view),
    path('logout/', logout_view),
    path('event_display/', event_display),
    path('create_event/', create_event),
    path('update_event/<int:pk>/', update_event),
    path('event_register/', event_register),
    path('event_interested/', event_interested),
    path('get_events_via_club/', get_events_via_club),
    path('club_display/', club_display),
    path('club_follow/', club_follow),
    path('club_unfollow/', club_unfollow),
    path('member_request/', create_member_request),
    path('member_request_verify/', member_request_validation),
    path('get_members_requested/', get_members_requested),
    path('remove_member/', remove_member),
    path('member_request_check/', member_request_check),
    path('fetch_club/', fetch_club),
    path('create_comment/', create_comment),
    path('interested_participated_events/', interested_participated_events),
    path('all_interested_participants/', all_interested_participants),
    path('get_event_via_id/', get_event_via_id),
]
