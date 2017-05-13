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
        email_domain_index = email.index('@')
        email_domain = email[email_domain_index:]
        vrpage = cleaned_data.get("vrpage")

        polished_email_for_vrpage = [
            polished_url.polished_email.lower()
            for polished_url in
            models.PolishedUrl.objects.filter(vrpage=vrpage)
        ]

        unsubscribes_for_vrpage = [
            unsubscribe.email.lower()
            for unsubscribe in
            models.Unsubscribed.objects.filter(vrpage=vrpage)
        ]

        unsubscribe_emails = [
            unsubscribe.email.lower()
            for unsubscribe in
            models.Unsubscribed.objects.filter(permanent=True)
        ]

        unsubscribe_domain = [
            domain.domain.lower()
            for domain in
            models.Unsubscribed.objects.filter(entire_domain=True)
        ]

        if email.lower() not in polished_email_for_vrpage:
            raise forms.ValidationError("Email is not registered for this VR Page")
        if email.lower() in unsubscribes_for_vrpage:
            raise forms.ValidationError("Email is already unsubscribed for this VR Page")
        if email.lower() in unsubscribe_emails:
            raise forms.ValidationError("Email is already unsubscribed permanently")
        if email_domain.lower() in unsubscribe_domain:
            raise forms.ValidationError("The domain {} has unsubscribed from our emails entirely".format(email_domain[1:]))


class UnsubscribePermanentlyForm(forms.ModelForm):
    class Meta:
        model = models.Unsubscribed
        fields = [
            'email'
        ]

    def clean(self):
        cleaned_data = super(UnsubscribePermanentlyForm, self).clean()
        email = cleaned_data.get("email")
        email_domain_index = email.index('@')
        email_domain = email[email_domain_index:]

        unsubscribe_emails = [
            unsubscribe.email.lower()
            for unsubscribe in
            models.Unsubscribed.objects.filter(permanent=True)
        ]

        unsubscribe_domain = [
            domain.domain.lower()
            for domain in
            models.Unsubscribed.objects.filter(entire_domain=True)
        ]

        if email.lower() in unsubscribe_emails:
            raise forms.ValidationError("Email is already unsubscribed permanently")
        if email_domain.lower() in unsubscribe_domain:
            raise forms.ValidationError("The domain {} has unsubscribed from our emails entirely".format(email_domain[1:]))


class UnsubscribeEntireDomainForm(forms.ModelForm):
    class Meta:
        model = models.Unsubscribed
        fields = [
            'domain'
        ]

    def clean(self):
        cleaned_data = super(UnsubscribeEntireDomainForm, self).clean()
        domain = cleaned_data.get("domain")

        domains = [
            domain.domain.lower()
            for domain in
            models.Unsubscribed.objects.filter(entire_domain=True)
        ]

        if domain.lower() in domains:
            raise forms.ValidationError(
                "The domain {} has unsubscribed from our emails entirely"
                .format(domain[1:])
            )

