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