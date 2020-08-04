from django.urls import path
from .views import current_user, UserList, EventList

urlpatterns = [
    path('current_user/', current_user),
    path('users/', UserList.as_view()),
    path('events/', EventList.as_view(), name='event_list'),
    # path('profile/<int:pk>/', ProfileDetail.as_view()),


]