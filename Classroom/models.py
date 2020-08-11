from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):

    college = models.CharField(max_length=50)
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_picture = models.FileField()

    def __str__(self):
        return f' {self.college}'


class Professor(models.Model):
    #First name being optional makes it easier to create a new section.
    first_name = models.CharField(max_length=50, blank=True, default='')
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.last_name}'


class Section(models.Model):

    Section = models.CharField(max_length=255)
    Name = models.CharField(max_length=255)
    Professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='sections')
    students = models.ManyToManyField(User, related_name='sections')


class ClassMeeting(models.Model):
    class_section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='meetings')
    date = models.DateField(default=timezone.now)


class Note(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    meeting = models.ForeignKey(ClassMeeting, on_delete=models.CASCADE, related_name='notes')
    description = models.CharField(max_length=200)
    text = models.TextField(max_length=1000, blank=True, null=True)
    file = models.FileField(blank=False, null=True)
    time = models.DateTimeField(default=timezone.now)


class Comment(models.Model):
    content = models.TextField(max_length=500)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    meeting = models.ForeignKey(ClassMeeting, on_delete=models.CASCADE, related_name='comments')
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='comments')
    time = models.DateTimeField(default=timezone.now)


class Event(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500, blank=True, null=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    location = models.CharField(max_length=100, blank=True, null=True)
    viewable = models.BooleanField()
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='events',
                             blank=True,
                             null=True)
    class_section = models.ForeignKey(Section,
                                      on_delete=models.CASCADE,
                                      related_name='events',
                                      blank=True,
                                      null=True)


class Review(models.Model):

    User = models.ForeignKey(User, on_delete=models.CASCADE)

    class_section = models.ForeignKey(Section, on_delete=models.CASCADE)

    description = models.TextField(max_length=1000)

    Professor = models.ForeignKey(Professor, on_delete=models.CASCADE)


class Alert(models.Model):
    read_status = models.BooleanField(default=False)
    message = models.CharField(max_length=55)
    event = models.ForeignKey(Event,
                              on_delete=models.CASCADE,
                              related_name='alert')
