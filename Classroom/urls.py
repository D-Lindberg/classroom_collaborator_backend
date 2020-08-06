from django.urls import path

from .views import current_user, UserList, EventList, EventDetail, NewEvent,ProfileDetail


urlpatterns = [
  

    path('profile/', ProfileDetail.as_view()),
    
    
    path('events/', EventList.as_view(), name='event_list'),
    path('events/<int:pk>', EventDetail.as_view(), name='event_detail'),
    path('events/new', NewEvent.as_view(), name='new_event'),
    

]