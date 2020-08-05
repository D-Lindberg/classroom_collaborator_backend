from django.urls import path
from .views import current_user, UserList, EventList, EventDetail, NewEvent, AlertList, AlertDetail

urlpatterns = [
    path('current_user/', current_user),
    path('users/', UserList.as_view()),
    path('events/', EventList.as_view(), name='event_list'),
    path('events/<int:pk>', EventDetail.as_view(), name='event_detail'),
    path('events/new', NewEvent.as_view(), name='new_event'),
    path('alerts/', AlertList.as_view(), name='alert_list'),
    path('alerts/<int:pk>', AlertDetail.as_view(), name='alert_detail'),
    # path('profile/<int:pk>/', ProfileDetail.as_view()),
]