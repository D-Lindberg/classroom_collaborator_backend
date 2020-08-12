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
import ipdb; 



def user_list(request):
    users = User.objects.all()
    return HttpResponse(users)


# Helper Function uses the information in the request to return information pertinent to the current user


def get_current_user(request):
    serializer = UserSerializer(request.user)
    current_user_id = serializer.data['id']
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
    # permission_classes = (permissions.AllowAny,)
    serializer_class = EventListSerializer

    def get_queryset(self):
        return self.request.user.events.all()


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (permissions.AllowAny,)
    serializer_class = EventDetailSerializer

    def get_queryset(self):
        return self.request.user.events.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        serializer.save()

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        serializer.save()


class NewEvent(generics.CreateAPIView):
    # permission_classes = (permissions.AllowAny,)
    queryset = Event.objects.all()
    serializer_class = NewEventSerializer

    def perform_create(self, serializer):
        event = serializer.save(user=self.request.user)
        alert = Alert(read_status=False, message='test', event=event)
        alert.save()

class SectionEventList(generics.ListCreateAPIView):
    # permission_classes = (permissions.AllowAny,)
    serializer_class = EventListSerializer
    def get_queryset(self):
        return Section.objects.get(id=self.kwargs['pk']).events.all()
        

class AlertList(generics.ListCreateAPIView):
    # permission_classes = (permissions.AllowAny,)
    serializer_class = AlertListSerializer

    def get_queryset(self):
        events = self.request.user.events.all()
        alerts = Alert.objects.filter(event__in=events).filter(
            read_status=False).order_by('event__start')
        return Alert.objects.filter(event__in=events).filter(read_status=False).order_by('event__start')


class AlertDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (permissions.AllowAny,)
    queryset = Alert.objects.all()
    serializer_class = AlertDetailSerializer


class NewNotes(generics.CreateAPIView):
    # permission_classes = (permissions.AllowAny,)
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = NewNoteSerializer
    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

class SectionDetail(generics.RetrieveAPIView):
    # queryset = Section.objects.all()
    serializer_class = SectionDetailSerializer
    def get_queryset(self):
        return self.request.user.sections.all()

class ProfileView(CreateAPIView):
    #parser_classes = (FileUploadParser, )
    serializer_class = UserProfileSerializer

    #parser_class = (FileUploadParser, )
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (permissions.AllowAny, )

    # serializer_class = NoteSerializer

    # parser_class = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        user = request.user
        queryset = Profile.objects.filter(username_id=user.id)
        serializer = UserProfileSerializer(queryset, many=True)
        if len(serializer.data) > 0:
            data = serializer.data[0]
        else:
            data = []

        return Response(data=data)

    def put(self, request, *args, **kwargs):
        user = request.user

        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        college = request.data.get('college', '')

        profile_picture = request.data.get('profile_picture', None)

        profile_ = Profile.objects.filter(username_id=request.user.id)

        if first_name:
            profile_.update(first_name=first_name)

        if last_name:
            profile_.update(last_name=last_name)

        if college:
            profile_.update(college=college)

        if profile_picture:
            user = Profile.objects.get(username_id=request.user.id)
            file = UserProfileSerializer(
                user, data={'profile_picture': profile_picture}, partial=True)
            file.is_valid(raise_exception=True)
            file.save()

        queryset = Profile.objects.filter(username_id=request.user.id)
        profile = UserProfileSerializer(queryset, many=True)

        return Response(data=profile.data, status=status.HTTP_200_OK)


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

    # create a queryset of all reviews for the current user
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
    # add the current sudent to the correct section
    current_section_object.students.add(current_user_object)

    return HttpResponse('Successfully added')


@csrf_exempt
@api_view(['GET', 'POST'])
def new_section(request):


    #POST REQUEST FROM REACT
        if request.method == "POST":
                #request.data is a json object from which we can access information to build a new section object
                section_title = request.data["Section"]
                section_name = request.data["SectionName"]
                professor = request.data["ProfessorLastName"]
                #If the Professor doesn't exist, create a new one
                Professor.objects.get_or_create(last_name=professor)
                #now get that professor
                ProfessorObject = Professor.objects.get(last_name=professor)
                #create the new review object which records it in the database
                new_Section = Section.objects.create(Section=section_title, Name=section_name, Professor=ProfessorObject)


                #Now add the current user to the class section
                current_user_object = get_current_user(request)
                new_Section.students.add(current_user_object)

                #this return is purely aesthetic. You can use the console-network-click the name of the request to see what the new review object looks like
                return HttpResponse(new_Section)
        else:
               return HttpResponse('This is a get request') 




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
                reviewed_professor = Professor.objects.get(sections=sectionID)
                
                #create the new review object which records it in the database
                new_review = Review.objects.create( User=current_user,class_section=reviewed_section, description=description, Professor=reviewed_professor)

                all_reviews_by_user = Review.objects.filter(User=current_user)

                # #Serialize the queryset all_reviews
                serialized_revs = ReviewSerializer(all_reviews_by_user).all_reviews
                # convert Serialized object to json
                print(Response(serialized_revs))
                return Response(serialized_revs)

#Michael Needs this for review creation on the front end

@api_view(['GET'])
def get_sections_for_current_user(request):
    current_user = get_current_user(request)
    my_class_sections = Section.objects.filter(students=current_user)
    serialized_sections = SectionSerializer(my_class_sections).all_sections
    return Response(serialized_sections)


@api_view(['GET'])
def all_reviews_by_professor(request, ProfID):
    reviewed_professor = Professor.objects.get(id=ProfID)
    # create a queryset of all reviews for the current user
    all_reviews_by_professor = Review.objects.filter(
        Professor=reviewed_professor)

    # #Serialize the queryset all_reviews
    serialized_recs = ReviewSerializer(all_reviews_by_professor).all_reviews

    # convert Serialized object to json

    return Response(serialized_recs)


@api_view(['GET'])
def get_professor(request, ProfID):
        ProfessorObject = Professor.objects.filter(id=ProfID)
        serialized_Professor = ProfessorSerializer(ProfessorObject).prof_detail
        return Response(serialized_Professor)
                

class ClassMeetingList(generics.ListCreateAPIView):

    # filter to first fake user until authentication is worked out
    queryset = ClassMeeting.objects.all()
    permission_classes = (permissions.AllowAny,)

    serializer_class = ClassMeetingSerializer


class MeetingComments(generics.ListCreateAPIView):
    serializer_class = MeetingCommentSerializer

    def get_queryset(self):
        return ClassMeeting.objects.get(id=self.kwargs['pk']).comments.filter(parent_comment__isnull=True).order_by('time')


class MeetingNotes(generics.ListCreateAPIView):
    serializer_class = NoteSerializer

    def get_queryset(self):
        return ClassMeeting.objects.get(id=self.kwargs['pk']).notes.all().order_by('time')

class NewComment(generics.CreateAPIView):
    # permission_classes = (permissions.AllowAny,)
    queryset = Comment.objects.all()
    serializer_class = NewCommentSerializer
    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class UserMeetings(generics.ListAPIView):

    serializer_class = UserMeetingsSerializer
    def get_queryset(self):
        sections = self.request.user.sections.all()
        return ClassMeeting.objects.filter(class_section__in=sections)

# class SectionMeetings(generics.ListAPIView):
#     serializer_class = 

@api_view(['POST'])
def create_meeting(request):
    serializer = ClassMeetingSerializer(data=request.data)
    if serializer.is_valid():
        class_meeting = serializer.save()
    return Response(serializer.data)

# extra?


@api_view(['DELETE'])
def delete_meeting(request, pk):
    class_meeting = ClassMeeting.objects.get(id=pk)
    class_meeting.delete()
    return Response('Class Meeting Deleted')
