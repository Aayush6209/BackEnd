from django.urls import path

from .views import *

urlpatterns = [
    path('register/', register_view),
    path('login/', login_view),
    path('logout/', logout_view),
    path('create_event/', create_event),
    path('update_event/<int:pk>/', update_event),
    path('event_register/', event_register),
    path('event_interested/', event_interested),
    path('club_follow/', club_follow),
    path('club_unfollow/', club_unfollow),
    path('member_request/', create_member_request),
    path('member_request_verify/', member_request_validation),
    path('create_comment/', create_comment)
]
