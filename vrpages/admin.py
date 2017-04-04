from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.VRPage)
admin.site.register(models.PolishedUrl)
admin.site.register(models.MessageTemplate)
admin.site.register(models.EmailMessage)
admin.site.register(models.Unsubscribed)