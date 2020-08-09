from django.urls import path
from .views import (
    current_user,
    all_reviews_by_user,
    all_reviews_by_professor,
    get_sections_for_current_user,
    all_sections,
    ProfileView,
    register,
    add_current_user_to_section,
    new_section,
    new_review,  #ProfileDetail 
    EventList,
    EventDetail,
    NewEvent,
    AlertList,
    AlertDetail,
    NewNotes,
    ProfessorList,
    NewProfessor,
    NewSection,
    SectionStudents,
    SectionList,
    MySectionList
    )

urlpatterns = [
    path('register/', register),
    path('current_user/', current_user),
    path('current_user/reviews/all', all_reviews_by_user),
    path('current_user/reviews/new', new_review),
    path('current_user/sections/all', get_sections_for_current_user),
    path('current_user/sections/<int:SectionID>/AddAStudent',
         add_current_user_to_section),
    path('reviews/<ProfID>', all_reviews_by_professor),
    
    # path('users/', UserList.as_view()),
    # path('profile/', ProfileDetail.as_view()),

    path('sections/new', new_section),
    path('sections/all', all_sections),
    path('profile/', ProfileView.as_view()),

    # path('users/', UserList.as_view()),
    # path('profile/', ProfileDetail.as_view()),
    path('events/', EventList.as_view(), name='event_list'),
    path('events/<int:pk>', EventDetail.as_view(), name='event_detail'),
    path('events/new', NewEvent.as_view(), name='new_event'),

    path('alerts/', AlertList.as_view(), name='alert_list'),
    path('alerts/<int:pk>', AlertDetail.as_view(), name='alert_detail'),
    
    path('notes/new', NewNotes.as_view(), name='new_notes'),
    
    path('professors/', ProfessorList.as_view(), name='professor_list'),
    path('professors/new', NewProfessor.as_view(), name='new_professor'),

    path('sections2/', SectionList.as_view(), name='section_list'),
    path('sections2/mine', MySectionList.as_view(), name='section_list'),
    path('sections2/new', NewSection.as_view(), name='new_section'),
    path('sections2/<int:pk>/students', SectionStudents.as_view(), name='section_students'),


    # path('profile/<int:pk>/', ProfileDetail.as_view()),
]