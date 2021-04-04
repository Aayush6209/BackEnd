from django.urls import path

from .views import *

urlpatterns = [
    path('register/', register_view),
    path('login/', login_view),
    path('logout/', logout_view),
    path('create_event/', create_event),
    path('update_event/<int:pk>/', update_event),
    path('club_follow/', club_follow),
    path('club_unfollow/', club_unfollow),
]
