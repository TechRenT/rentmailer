from django.core.urlresolvers import reverse
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

    def __str__(self):
        return self.vrpage_name

    def get_absolute_url(self):
        return reverse("vrpages:vrpage_detail", kwargs={"pk": self.pk})


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

    def __str__(self):
        return self.polished_url


class MessageTemplate(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    vrpage = models.ForeignKey(VRPage)
    template_type = models.CharField(max_length=10)
    subject = models.CharField(max_length=255)
    message_body = models.TextField()

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse("vrpages:template_detail", kwargs={"pk": self.pk})


class EmailMessage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message_body = models.TextField()
    message_type = models.CharField(max_length=10)
    polished_url = models.ForeignKey(PolishedUrl)

    def __str__(self):
        return self.email


class Unsubscribed(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=True, null=True)
    vrpage = models.ForeignKey(VRPage, blank=True, null=True)
    permanent = models.BooleanField(default=False)
    domain = models.CharField(max_length=50, blank=True)
    entire_domain = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "unsubscribes"

    def __str__(self):
        if self.email:
            return self.email
        elif self.domain:
            return self.domain

