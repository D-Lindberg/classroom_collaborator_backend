from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.Professor)
admin.site.register(models.Section)
admin.site.register(models.ClassMeeting)
admin.site.register(models.Note)
admin.site.register(models.Comment)
admin.site.register(models.Event)
admin.site.register(models.Review)
admin.site.register(models.Alert)
