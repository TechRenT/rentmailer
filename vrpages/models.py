from django.db import models

# Create your models here.
class VRPage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    vrpage_name = models.CharField(max_length=255)
    email_address = models.EmailField()
    email_username = models.CharField(max_length=255)
    email_password = models.CharField(max_length=50)
    email_server = models.CharField(max_length=50)
    email_from_name = models.CharField(max_length=50)

