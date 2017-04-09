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

    # def clean(self):
    #     cleaned_data = super(LinkedinProfileForm, self).clean()
    #     profile_link = cleaned_data.get("profile_link")

    #     profile_list = [str(profile) for profile in models.LinkedinProfile.objects.all()]

    #     if profile_link in profile_list:
    #         raise forms.ValidationError("This profile already exist in our database!")