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
from django.views.decorators.csrf import csrf_exempt





def user_list(request):
    users = User.objects.all()
    return HttpResponse(users)




#Helper Function uses the information in the request to return information pertinent to the current user

def get_current_user(request):
    serializer = UserSerializer(request.user)
    current_user_username=serializer.data['username']
    print(User.objects.get(username=current_user_username))
    return User.objects.get(username=current_user_username)


@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)




 


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
    
    
    

# Returns a Json Response of all Reviews associated with a User 
@api_view(['GET'])
def all_reviews_by_user(request):
    
        current_user_object = get_current_user(request)

        #create a queryset of all reviews for the current user
        all_reviews_by_user = Review.objects.filter(User=current_user_object)
        
        # #Serialize the queryset all_reviews
        serialized_recs = ReviewSerializer(all_reviews_by_user).all_reviews
        
        # convert Serialized object to json

        return Response(serialized_recs)


@api_view(['GET'])
def all_reviews_by_professor(request, ProfID):
        reviewed_professor = Professor.objects.get(id=ProfID)
        #create a queryset of all reviews for the current user
        all_reviews_by_professor = Review.objects.filter(Professor=reviewed_professor)
        print(all_reviews_by_professor)
        
        # #Serialize the queryset all_reviews
        serialized_recs = ReviewSerializer(all_reviews_by_professor).all_reviews
        
        # convert Serialized object to json

        return Response(serialized_recs)

@csrf_exempt
@api_view(['GET','POST'])
def new_review(request):
        #POST REQUEST FROM REACT
        if request.method == "POST":
                #current autheticated user helper function
                current_user = get_current_user(request)
                
                #section from the body? of the post request
                sectionID = request.data["sectionID"]
                #Use this info to get ahold of the section object
                reviewed_section = Section.objects.get(id=sectionID)

                #description from the body of the post request
                description = request.data["description"]

                #professor info through the same process as section
                professor = request.data["ProfessorID"]
                reviewed_professor = Professor.objects.get(id=professor)

                #create the new review object which records it in the database
                new_review = Review.objects.create( User=current_user,class_section=reviewed_section, description=description, Professor=reviewed_professor)

                #this return is purely aesthetic. You can use the console-network-click the name of the request to see what the new review object looks like
                return HttpResponse(new_review)





    

