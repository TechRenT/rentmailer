from django import forms

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
