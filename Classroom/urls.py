from django.urls import path
from .views import (
    current_user,
    all_reviews_by_user,
    all_reviews_by_professor,
    EventList,
    EventDetail,
    NewEvent,
    AlertList,
    AlertDetail,
    get_sections_for_current_user,
    all_sections,
    ProfileView,
    register,
    add_current_user_to_section,
    new_section,
    AlertList,
    AlertDetail,
    new_review, 
    get_professor, #ProfileDetail,
    SectionDetail,
    SectionEventList,
    ClassMeetingList,
    # ClassMeetingDetail,
    # create_meeting,
    MeetingComments,
    MeetingNotes,
    UserMeetings,
    NewComment,
    NewNotes,
    CreateMeeting,
)

urlpatterns = [
    path('register/', register),
    path('current_user/', current_user),
    path('current_user/reviews/all', all_reviews_by_user),
    path('current_user/reviews/new', new_review),
    path('current_user/sections/all', get_sections_for_current_user),
    path('current_user/sections/<int:SectionID>/AddAStudent',
         add_current_user_to_section),
    path('current_user/meetings', UserMeetings.as_view()),
    path('reviews/<ProfID>', all_reviews_by_professor),
    path('Professor/<ProfID>', get_professor),
    path('sections/new', new_section),
    path('sections/all', all_sections),
    path('sections/<int:pk>', SectionDetail.as_view()),
    path('sections/<int:pk>/events', SectionEventList.as_view()),
    path('sections/<int:pk>/meetings', SectionEventList.as_view()),
    path('profile/', ProfileView.as_view()),
    # path('users/', UserList.as_view()),
    # path('profile/', ProfileDetail.as_view()),
    path('events/', EventList.as_view(), name='event_list'),
    path('events/<int:pk>', EventDetail.as_view(), name='event_detail'),
    path('events/new', NewEvent.as_view(), name='new_event'),
    path('alerts/', AlertList.as_view(), name='alert_list'),
    path('alerts/<int:pk>', AlertDetail.as_view(), name='alert_detail'),
    path('meetings/', ClassMeetingList.as_view()),
    path('meetings/<int:pk>/comments', MeetingComments.as_view()),
    path('meetings/<int:pk>/notes', MeetingNotes.as_view()),
    path('meetings/new', CreateMeeting.as_view()),
    path('comments/new', NewComment.as_view(), name='new_event'),
    path('notes/new', NewNotes.as_view(), name='new_notes'),
    # path('profile/<int:pk>/', ProfileDetail.as_view()),
]