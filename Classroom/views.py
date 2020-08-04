from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from rest_framework import permissions, status , viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken
from rest_framework.parsers import MultiPartParser
from .serializers  import *
from .models import *





def user_list(request):
    users = User.objects.all()
    return HttpResponse(users)




#Helper Function uses the information in the request to return information pertinent to the current user

def get_current_user(request):
    serializer = UserSerializer(request.user)
    current_user_username=serializer.data['username']
    return User.objects.get(username=current_user_username)


@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


def userFromId(userID):
    return User.objects.get(id=userID)

class EventList(generics.ListCreateAPIView):
    
    # filter to first fake user until authentication is worked out
    queryset = Event.objects.filter(user=User.objects.all()[0])
    permission_classes = (permissions.AllowAny,)


    serializer_class = EventListSerializer


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    # filter to first fake user until authentication is worked out
    queryset = Event.objects.filter(user=User.objects.all()[0])
    serializer_class = EventDetailSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        serializer.save(category=userFromId(
            serializer.initial_data['userID']))
        serializer.save()

    def perform_update(self, serializer):
        serializer.save(category=userFromId(
            serializer.initial_data['userID']))
        serializer.save()

 

class NewEvent(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = NewEventSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        serializer.save(user=userFromId(
            serializer.initial_data['userID']))

class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    
    
    # class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    #     queryset = Profile.objects.all()
    #     serializer_class = ProfileSerializer
    
    
    

#Returns a Json Response of all Reviews associated with a User 
# @api_view(['GET'])
# def all_reviews_by_user(request):
    
#         current_user_object = get_current_user(request)

#         #create a queryset of all reviews for the current user
#         all_reviews = Review.objects.filter(user=current_user_object)
        
#         #Serialize the queryset all_reviews
#         serialized_recs = ReviewSerializer(all_reviews).all_reviews
        
#         # convert Serialized object to json


#         return Response(serialized_recs)





    

