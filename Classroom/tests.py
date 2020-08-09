from django.test import TestCase
from django.contrib.auth.models import User
# Create your tests here.
from .models import *


class ProfileModelTest(TestCase):


    @classmethod
    def setUpTestData(cls):
        Profile.objects.create(first_name='Osei', last_name='Amoabin', username=user, college = 'University of Texas', profile_picture='/image.jpeg')
        
        
        
    def test_profile_content(self):
        profile = Profile.objects.get(id=1)
        expected_object_name= f'{profile.first_name}'
        self.assertEquals(expected_object_name, 'Osei')
       