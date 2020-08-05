from Classroom.models import Event, Alert
from django.contrib.auth.models import User
from django.utils import timezone

User.objects.all().delete()
Event.objects.all().delete()

u1 = User(username='john')
u1.save()

u2 = User(username='sarah')
u2.save()

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