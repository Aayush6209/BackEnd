from django.urls import path

from .views import register_view, login_view, logout_view, create_event, update_event

urlpatterns = [
    path('register/', register_view),
    path('login/', login_view),
    path('logout/', logout_view),
    path('create_event/', create_event),
    path('update_event/<int:pk>/', update_event),
]
