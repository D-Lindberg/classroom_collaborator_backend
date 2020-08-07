from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from rest_framework import permissions, status, viewsets, generics
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer, UserSerializerWithToken
from rest_framework.parsers import MultiPartParser, FileUploadParser, FormParser
from .serializers import *
from .models import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated, AllowAny


def user_list(request):
    users = User.objects.all()
    return HttpResponse(users)


#Helper Function uses the information in the request to return information pertinent to the current user


def get_current_user(request):
    serializer = UserSerializer(request.user)
    current_user_id = serializer.data['id']
    print(User.objects.get(id=current_user_id))
    return User.objects.get(id=current_user_id)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    # permission_classes = (permissions.AllowAny, )

    serializer = UserSerializerWithToken(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    permission_classes = (permissions.AllowAny, )

    serializer_class = EventListSerializer


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    # filter to first fake user until authentication is worked out
    queryset = Event.objects.filter(user=User.objects.all()[0])
    serializer_class = EventDetailSerializer
    permission_classes = (permissions.AllowAny, )

    def perform_create(self, serializer):
        serializer.save(category=userFromId(serializer.initial_data['userID']))
        serializer.save()

    def perform_update(self, serializer):
        serializer.save(category=userFromId(serializer.initial_data['userID']))
        serializer.save()


class NewEvent(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = NewEventSerializer
    permission_classes = (permissions.AllowAny, )

    def perform_create(self, serializer):
        event = serializer.save(
            user=userFromId(serializer.initial_data['userID']))
        alert = Alert(read_status=False, message='test', event=event)
        alert.save()


class AlertList(generics.ListCreateAPIView):

    # filter to first fake user until authentication is worked out
    events = Event.objects.filter(user=User.objects.all()[0])
    queryset = Alert.objects.filter(event__in=events).filter(
        read_status=False).order_by('event__start')
    permission_classes = (permissions.AllowAny, )

    serializer_class = AlertListSerializer


class AlertDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertDetailSerializer
    permission_classes = (permissions.AllowAny, )


class ProfileView(CreateAPIView):
    #parser_classes = (FileUploadParser, MultiPartParser)
    serializer_class = UserProfileSerializer

    parser_classes = (MultiPartParser, FormParser)
    #permission_classes = (permissions.AllowAny,)
    #serializer_class = NoteSerializer

    #parser_class = (MultiPartParser, FormParser)

    # def post(self, request, *args, **kwargs):

    #     serializer = UserProfileSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors,
    #                         status=status.HTTP_400_BAD_REQUEST)

    # def get(self, request, *args, **kwargs):
    #     user = request.user
    #     queryset = Profile.objects.filter(username_id=user.id)
    #     serializer = UserProfileSerializer(queryset, many=True)
    #     if len(serializer.data) > 0:
    #         data = serializer.data[0]
    #     else:
    #         data = []

    #     return Response(data=data)


# class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = UserSerializer

#     def get(self, request, pk=None):
#         user = request.user
#         queryset = Profile.objects.filter(username_id=user.id)
#         serializer = UserProfileSerializer(queryset, many=True)
#         return Response(data=serializer.data[0])


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
def all_sections(request):

    all_class_sections = Section.objects.all()

    serialized_sections = SectionSerializer(all_class_sections).all_sections

    return Response(serialized_sections)


@api_view(['GET'])
def add_current_user_to_section(request, SectionID):
    current_user_object = get_current_user(request)
    current_section_object = Section.objects.get(id=SectionID)
    #add the current sudent to the correct section
    current_section_object.students.add(current_user_object)

    return HttpResponse('Successfully added')


@csrf_exempt
@api_view(['GET', 'POST'])
def new_section(request):
    #POST REQUEST FROM REACT
    if request.method == "POST":

        #request.data is a json object from which we can access information to build a new section object

        section_title = request.data["Section"]

        professor = request.data["ProfessorID"]
        ProfessorObject = Professor.objects.get(id=professor)

        #create the new review object which records it in the database
        new_Section = Section.objects.create(Section=section_title,
                                             Professor=ProfessorObject)

        #Now add the current user to the class section
        current_user_object = get_current_user(request)
        new_Section.students.add(current_user_object)

        #this return is purely aesthetic. You can use the console-network-click the name of the request to see what the new review object looks like
        return HttpResponse(new_Section)


@api_view(['GET'])
def all_reviews_by_professor(request, ProfID):
    reviewed_professor = Professor.objects.get(id=ProfID)
    #create a queryset of all reviews for the current user
    all_reviews_by_professor = Review.objects.filter(
        Professor=reviewed_professor)
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

#Michael Needs this for review creation on the front end
@api_view(['GET'])
def get_sections_for_current_user(request):
    current_user = get_current_user(request)

    my_class_sections = Section.objects.filter(students=current_user)

    serialized_sections = SectionSerializer(my_class_sections).all_sections
    print(serialized_sections)
    return Response(serialized_sections)


@api_view(['GET'])
def all_reviews_by_professor(request, ProfID):
    reviewed_professor = Professor.objects.get(id=ProfID)
    #create a queryset of all reviews for the current user
    all_reviews_by_professor = Review.objects.filter(
        Professor=reviewed_professor)
    print(all_reviews_by_professor)

    # #Serialize the queryset all_reviews
    serialized_recs = ReviewSerializer(all_reviews_by_professor).all_reviews

    # convert Serialized object to json

    return Response(serialized_recs)


@csrf_exempt
@api_view(['GET', 'POST'])
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
        new_review = Review.objects.create(User=current_user,
                                           class_section=reviewed_section,
                                           description=description,
                                           Professor=reviewed_professor)

        #this return is purely aesthetic. You can use the console-network-click the name of the request to see what the new review object looks like
        return HttpResponse(new_review)
