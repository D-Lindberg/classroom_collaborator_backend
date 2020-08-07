from Classroom.models import Event, Professor, Section, Review, Alert, ClassMeeting
from django.contrib.auth.models import User
from django.utils import timezone

User.objects.all().delete()
Event.objects.all().delete()

u1 = User(username='john')
u1.save()

u2 = User(username='sarah')
u2.save()

p1 = Professor(first_name='Mr', last_name ="Professorson")
p1.save()

p2 = Professor(first_name='Mrs', last_name ="ProfessorWoman")
p2.save()

Sec1 = Section(Section="A1234", Professor = p2, )
Sec1.save()
Sec1.students.add(u1)
Sec1.students.add(u2)
Sec1.save()

Rev1 = Review(User = u1, class_section=Sec1, description="I feel a deep hatred for mr professorson and for this class", Professor=p1)

Rev2 = Review(User = u2, class_section=Sec1, description="I also feel a deep hatred for mr professorson and for his class", Professor=p1)

Rev1.save()
Rev2.save()




e1 = Event(
    title='event1',
    description='test event1',
    start=timezone.make_aware(timezone.datetime(2020, 8, 10, 14, 30)),
    end=timezone.make_aware(timezone.datetime(2020, 8, 10, 18, 0)),
    location='mars',
    viewable=True,
    user=u1
    )
e1.save()

e2 = Event(
    title='event2',
    description='test event2',
    start=timezone.make_aware(timezone.datetime(2020, 8, 15, 8, 0)),
    end=timezone.make_aware(timezone.datetime(2020, 8, 18, 16, 0)),
    location='moon',
    viewable=False,
    user=u1
    )
e2.save()

a1 = Alert(message='test', event=e1)
a1.save()
a2 = Alert(message='test', event=e2)
a2.save()

meeting = ClassMeeting(class_section=Sec1)
meeting.save()