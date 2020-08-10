from Classroom.models import *
from django.contrib.auth.models import User
from django.utils import timezone


#users
u1 = User(username='john', email='john@gmail.com')
u1.set_password('11')
u1.save()
u2 = User(username='sarah', email='sarah@gmail.com')
u2.set_password('11')
u2.save()
u3 = User(username='mike', email='sarah@gmail.com')
u3.set_password('11')
u3.save()

#professors
p1 = Professor(first_name='Paul', last_name ="Ronney")
p1.save()
p2 = Professor(first_name='Geoffrey', last_name ="Shiflett")
p2.save()

#sections
sec1 = Section(Section="28725R", Name='AME 301: Dynamics', Professor = p1, )
sec1.save()
sec1.students.add(u1)
sec1.students.add(u2)
sec1.save()
sec2 = Section(Section="28726R", Name='AME 301: Dynamics', Professor = p2, )
sec2.save()
sec2.students.add(u1)
sec2.students.add(u2)
sec2.students.add(u3)
sec2.save()

#reviews
rev1 = Review(User = u1, class_section=sec1, description="I feel a deep hatred for mr professorson and for this class", Professor=p1)
rev2 = Review(User = u2, class_section=sec1, description="I also feel a deep hatred for mr professorson and for his class", Professor=p1)
rev1.save()
rev2.save()

#events
e1 = Event(
    title='study session',
    description='study session for the midterm',
    start=timezone.make_aware(timezone.datetime(2020, 8, 10, 14, 30)),
    end=timezone.make_aware(timezone.datetime(2020, 8, 10, 18, 0)),
    location='library',
    viewable=True,
    user=u1
    )
e1.save()

e2 = Event(
    title='homework help',
    description='work on homework together',
    start=timezone.make_aware(timezone.datetime(2020, 8, 15, 8, 0)),
    end=timezone.make_aware(timezone.datetime(2020, 8, 15, 16, 0)),
    location='starbucks',
    viewable=False,
    user=u1
    )
e2.save()

e3 = Event(
    title='midterm',
    description='2nd midterm of the semester',
    start=timezone.make_aware(timezone.datetime(2020, 8, 12, 16, 0)),
    end=timezone.make_aware(timezone.datetime(2020, 8, 12, 18, 0)),
    location='SAL 101',
    viewable=True,
    class_section=sec1
    )
e3.save()

e4 = Event(
    title='final project',
    description='final project due',
    start=timezone.make_aware(timezone.datetime(2020, 8, 14, 12, 0)),
    end=timezone.make_aware(timezone.datetime(2020, 8, 14, 12, 0)),
    location='SAL 101',
    viewable=True,
    class_section=sec1
    )
e4.save()

#alerts
a1 = Alert(message='', event=e1)
a2 = Alert(message='', event=e2)
a3 = Alert(message='', event=e3)
a4 = Alert(message='', event=e4)
a1.save()
a2.save()
a3.save()
a4.save()