from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from .models import *
from builtins import object


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'start', 'end', 'location',
                  'viewable')


class EventDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'start', 'end', 'location',
                  'viewable', 'user')


class NewEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('title', 'description', 'start', 'end', 'location',
                  'viewable', 'user')


class AlertListSerializer(serializers.ModelSerializer):
    event_time = serializers.SerializerMethodField('get_event_start')
    event_title = serializers.SerializerMethodField('get_event_title')

    def get_event_start(self, obj):
        return obj.event.start

    def get_event_title(self, obj):
        return obj.event.title

    class Meta:
        model = Alert
        fields = ('id', 'read_status', 'message', 'event_time', 'event_title')


class AlertDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ('id', 'read_status')


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
       serializer = self.parent.parent.__class__(value, context=self.context)
       return serializer.data

class MeetingCommentSerializer(serializers.ModelSerializer):
    comments = RecursiveField(many=True, required=False)
    username = serializers.SerializerMethodField('get_student_name')
    
    def get_student_name(self, obj):
        return obj.student.username

    class Meta:
        model = Comment
        fields = ('id', 'content', 'student', 'comments', 'username', 'parent_comment')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', )


class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        extra_kwargs = {"password": {"write_only": True}}

        model = User
        fields = (
            'token',
            'username',
            'password',
        )


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'first_name',
            'last_name',
            'username',
            'college',
            'profile_picture',
        )


class ProfessorSerializer(object):
    def __init__(self, body):
        self.body = body


    @property
    def prof_detail(self):
        output = {'Professor': []}

        for Professor in self.body:
            prof_detail = {
                'Prof_ID': Professor.id,
                'first_name': Professor.first_name,
                'Last_name': Professor.last_name,
            
            }
            output['Professor'].append(prof_detail)

        return output


class SectionSerializer(object):
    def __init__(self, body):
        self.body = body

    @property
    def all_sections(self):
        output = {'sections': []}

        for section in self.body:
            section_detail = {
                    'ID': section.id,
                'Section': section.Section,
                'Professor': section.Professor.last_name,
                'ProfID': section.Professor.id,
                'Name': section.Name,
                # 'students': section.students.username,
            }
            output['sections'].append(section_detail)

        return output

    @property
    def section_detail(self):
        output = {'section': []}

        for section in self.body:
            section_detail = {
                'Section': section.Section,
                'Professor': section.Professor,
                'ProfID': section.Professor.id,
                'students': section.students,
            }
            output['section'].append(section_detail)

        return output


class ClassMeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassMeeting
        fields = ('class_section', 'date')


class NoteSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')
    
    def get_username(self, obj):
        return obj.student.username

    class Meta:
        model = Note
        fields = ('student', 'username', 'meeting', 'description', 'text', 'file')

class NewNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('meeting', 'description', 'text', 'file')

class NewCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('meeting', 'content', 'parent_comment')

# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = ('__all__', )


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('__all__', )


class ReviewSerializer(object):
    def __init__(self, body):
        self.body = body

    @property
    def all_reviews(self):
        output = {'reviews': []}

        for review in self.body:
            review_detail = {
                'student': review.User.username,
                'section': review.class_section.Section,
                'description': review.description,
                'Professor': review.Professor.last_name,
                'ProfID': review.Professor.id
            }
            output['reviews'].append(review_detail)

        return output

    @property
    def review_detail(self):
        output = {'review': []}

        for review in self.body:
            review_detail = {
                'student': review.User,
                'section': review.class_section.Section,
                'description': review.description,
                'Professor': review.Professor.last_name,
                'ProfID': review.Professor.id
            }
            output['review'].append(review_detail)

        return output


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ('__all__', )


class SectionDetailSerializer(serializers.ModelSerializer):
    professor_first_name = serializers.SerializerMethodField('get_professor_first_name')
    professor_last_name = serializers.SerializerMethodField('get_professor_last_name')
    meeting = serializers.SerializerMethodField('get_meeting')

    def get_professor_first_name(self, obj):
        return obj.Professor.first_name

    def get_professor_last_name(self, obj):
        return obj.Professor.last_name

    def get_meeting(self, obj):
        return obj.meetings.values('date', 'id')

    class Meta:
        model = Section
        fields = ('id', 'Section', 'Name', 'professor_first_name', 'professor_last_name', 'meeting')

    

class UserMeetingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClassMeeting
        fields = ('id',)