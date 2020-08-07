# Generated by Django 3.0.8 on 2020-08-06 20:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Classroom', '0002_auto_20200806_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='parent_comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='Classroom.Comment'),
        ),
        migrations.AlterField(
            model_name='note',
            name='meeting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='Classroom.ClassMeeting'),
        ),
        migrations.AlterField(
            model_name='note',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to=settings.AUTH_USER_MODEL),
        ),
    ]
