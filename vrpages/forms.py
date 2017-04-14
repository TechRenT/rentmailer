from django import forms
from django.core.exceptions import ObjectDoesNotExist

from . import models


class SendEmailForm(forms.ModelForm):
    class Meta:
        model = models.EmailMessage
        fields = [
            'email',
            'subject',
            'message_body'    
        ]


class UnsubscribeFromVRPageForm(forms.ModelForm):
    class Meta:
        model = models.Unsubscribed
        fields = [
            'email',
            'vrpage'
        ]

    def clean(self):
        cleaned_data = super(UnsubscribeFromVRPageForm, self).clean()
        email = cleaned_data.get("email")
        vrpage = cleaned_data.get("vrpage")

        polished_email_for_vrpage = [
            polished_url.polished_email.lower()
            for polished_url in
            models.PolishedUrl.objects.filter(vrpage=vrpage)
        ]
        if email.lower() not in polished_email_for_vrpage:
            raise forms.ValidationError("Email is not registered for this VR Page")

        unsubscribes_for_vrpage = [
            unsubscribe.email.lower()
            for unsubscribe in
            models.Unsubscribed.objects.filter(vrpage=vrpage)
        ]
        if email.lower() in unsubscribes_for_vrpage:
            raise forms.ValidationError("Email is already unsubscribed for this VR Page")


class UnsubscribePermanentlyForm(forms.ModelForm):
    class Meta:
        model = models.Unsubscribed
        fields = [
            'email'
        ]


class UnsubscribeEntireDomainForm(forms.ModelForm):
    class Meta:
        model = models.Unsubscribed
        fields = [
            'domain'
        ]
