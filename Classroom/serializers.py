from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from .models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)


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
        model = User
        fields = ('token', 'username',)
        
        
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'username', 'college', 'profile_picture',)


class ProfessorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Professor
        fields = ('__all__',)


class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = ('__all__',)


class ClassMeetingSerializer (serializers.ModelSerializer):
    class Meta:
        model = ClassMeeting
        fields = ('__all__',)


class NoteSerializer (serializers.ModelSerializer):
    class Meta:
        model = Note
        fields =('__all__',)


class CommentSerializer (serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('__all__',)


class EventSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        fields = ('__all__',)


class ReviewSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model  = Review
        fields = ('__all__',)
        
        
class AlertSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Alert
        fields =('__all__',)
    
