from django.urls import path
from .views import current_user, UserList, all_reviews_by_user,all_reviews_by_professor

urlpatterns = [
    path('current_user/', current_user),
    path('current_user/reviews/all', all_reviews_by_user),
    path('reviews/<ProfID>', all_reviews_by_professor),

    path('users/', UserList.as_view()),
    # path('profile/<int:pk>/', ProfileDetail.as_view()),


]