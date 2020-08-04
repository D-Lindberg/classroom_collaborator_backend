from django.db import models
from django.contrib.auth.models import User






#This Profile class is how you can extend the built in django User class. Attributes can be accessed via 
# >>> u = User.objects.get(username='fsmith')
# >>> SmithsProfilePic = u.Profile.ProfPic
# https://www.geeksforgeeks.org/imagefield-django-models/ image field reference


class Profile(models.Model):
        first_name = models.CharField(max_length=50, default = "first_name")
        last_name = models.CharField(max_length=50, default = "last_name")
        college = models.CharField(max_length=50)
        username = models.OneToOneField(User, on_delete=models.CASCADE)
        profile_picture = models.ImageField()
        
        def __str__(self):
            return f'{self.first_name} {self.last_name}'
                   
                   
class Professor(models.Model):
        first_name = models.CharField(max_length=50)
        last_name = models.CharField(max_length=50)
        
        
        def __str__(self):
            return f'{self.first_name} {self.last_name}'
        
class Section(models.Model):
        Section = models.CharField(max_length=255)
        Professor =models.ForeignKey(Professor, on_delete=models.CASCADE) 
        students = models.ManyToManyField(User)

class ClassMeeting(models.Model):
    class_section = models.ForeignKey(Section, on_delete=models.CASCADE)

class Note(models.Model):
        #Subject to Change due to hosting of Images of notes
        # Content Object
        content = models.TextField(max_length=500) 
        student = models.ForeignKey(User, on_delete=models.CASCADE) 
        meeting = models.ForeignKey(ClassMeeting, on_delete=models.CASCADE)

class Comment(models.Model):
        content = models.TextField(max_length=500)
        student = models.ForeignKey(User, on_delete=models.CASCADE) 
        note = models.ForeignKey(Note, on_delete=models.CASCADE) 
        #I think the below is how you create a self reference to another instance of the same class
        parent_comment = models.ForeignKey('self', on_delete=models.CASCADE)

class Event(models.Model): 
        Event_Name = models.CharField(max_length=50)
        Event_Description = models.TextField(max_length=500)
        #We can potentially change DateField to include a time but...scope.
        Event_Date = models.DateField()
        class_section = models.ForeignKey(Section, on_delete=models.CASCADE)

class Review(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    description = models.TextField(max_length=500)

class Alert(models.Model):
        #Relations will be decided and added with the alerts User Story
        read_status = models.BooleanField()
        message = models.CharField(max_length=50)
