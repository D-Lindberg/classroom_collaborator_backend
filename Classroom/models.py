from django.db import models
from django.contrib.auth.models import User




class Profile(models.Model):

        first_name = models.CharField(max_length=50, default = "first_name")
        last_name = models.CharField(max_length=50, default = "last_name")
        college = models.CharField(max_length=50)
        username = models.OneToOneField(User, on_delete=models.CASCADE)
        profile_picture = models.ImageField()
        
        def __str__(self):
            return f'{self.first_name} {self.last_name} {self.college}'
                   
                   


class Professor(models.Model):
      first_name = models.CharField(max_length=50)
      last_name = models.CharField(max_length=50)

      def __str__(self):
          return f'{self.first_name} {self.last_name}'


class Section(models.Model):

    Section = models.CharField(max_length=255)
    Professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    students = models.ManyToManyField(User)


class ClassMeeting(models.Model):
        class_section = models.ForeignKey(Section, on_delete=models.CASCADE)


class Note(models.Model):
    # Subject to Change due to hosting of Images of notes
    # Content Object
    content = models.TextField(max_length=500)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    meeting = models.ForeignKey(ClassMeeting, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.TextField(max_length=500)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    # I think the below is how you create a self reference to another instance of the same class
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE)


class Event(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500, blank=True, null=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    location = models.CharField(max_length=100, blank=True, null=True)
    viewable = models.BooleanField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='events', blank=True, null=True)
    class_section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name='events', blank=True, null=True)


class Review(models.Model):

        User = models.ForeignKey(User, on_delete=models.CASCADE)

        class_section = models.ForeignKey(Section, on_delete=models.CASCADE)

        description = models.TextField(max_length=1000)

        Professor =models.ForeignKey(Professor, on_delete=models.CASCADE) 

class Alert(models.Model):
    read_status = models.BooleanField(default=False)
    message = models.CharField(max_length=50)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='alert')
