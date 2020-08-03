from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# add a few more attributes to User Model

# UserID pk
# Username string
# Password string
# First_Name string
# Last_Name string
# College string





class Professor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


class Section(models.Model):
    section = models.CharField(max_length=255)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
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
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    # We can potentially change DateField to include a time but...scope.
    date = models.DateField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE)


class Review(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    description = models.TextField(max_length=500)


class Alert(models.Model):
    # Are we relating alerts to Events? Unsure how to frame this
    # Still need to add relations here
    # Alert related to user

    # Every User in a Section gets a many to many relation to an alert which is related to a single event

    status = models.BooleanField()
    message = models.CharField(max_length=50)
