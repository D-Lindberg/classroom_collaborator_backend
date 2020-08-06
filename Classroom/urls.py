from django.urls import path

from .views import current_user, UserList, all_reviews_by_user,all_reviews_by_professor, EventList, EventDetail, NewEvent,ProfileDetail,get_sections_for_current_user, add_current_user_to_section,new_section,  AlertList, AlertDetail



urlpatterns = [
    path('current_user/', current_user),
    path('current_user/reviews/all', all_reviews_by_user),
    path('current_user/sections/all', get_sections_for_current_user),
    path('current_user/sections/<int:SectionID>/AddAStudent', add_current_user_to_section),
    path('reviews/<ProfID>', all_reviews_by_professor),
    path('sections/new', new_section),
    path('users/', UserList.as_view()),
    path('profile/', ProfileDetail.as_view()),
    path('events/', EventList.as_view(), name='event_list'),
    path('events/<int:pk>', EventDetail.as_view(), name='event_detail'),
    path('events/new', NewEvent.as_view(), name='new_event'),
    path('alerts/', AlertList.as_view(), name='alert_list'),
    path('alerts/<int:pk>', AlertDetail.as_view(), name='alert_detail'),
    # path('profile/<int:pk>/', ProfileDetail.as_view()),
]