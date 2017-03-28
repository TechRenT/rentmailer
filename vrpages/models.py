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


class PolishedUrl(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    vrpage = models.ForeignKey(VRPage)
    polished_url = models.URLField(max_length=200)
    polished_email = models.EmailField()
    page_title = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=30)
    anchor_text = models.CharField(max_length=255)
    first_message_sent = models.BooleanField(default=False)
    second_message_sent = models.BooleanField(default=False)
    unsubscribe_permanently = models.BooleanField(default=False)
    unsubscribe_from_vrpage = models.BooleanField(default=False)


class MessageTemplate(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    vrpage = ForeignKey(VRPage)
    template_type = models.CharField(max_length=10)
    subject = models.CharField(max_length=255)
    message_body = models.TextField()