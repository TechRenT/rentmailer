from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import forms
from . import models

# Create your views here.
def send_email(request):
    message_template = models.MessageTemplate.objects.get(vrpage_id=1)
    polished_url = models.PolishedUrl.objects.get(vrpage_id=1)
    message_variables = {'contactname': polished_url.contact_name,
                         'url': polished_url.polished_url,
                         'anchortext': polished_url.anchor_text,
                         'pagetitle': polished_url.page_title
                         }
    message_subject = message_template.subject.format(**message_variables)
    message_body = message_template.message_body.format(**message_variables)
    form = forms.SendEmailForm(initial={'email': polished_url.polished_email,
                                        'subject': message_subject,
                                        'message': message_body})
    if request.method == 'POST':
        form = forms.SendEmailForm(request.POST)
        if form.is_valid():
            send_mail(
                form.cleaned_data['subject'],
                form.cleaned_data['message'],
                '{} <{}>'.format('Renelle Tigue', 'purpose.renelle@gmail.com'),
                [form.cleaned_data['email']],
                fail_silently=False,
                auth_user='purpose.renelle@gmail.com',
                auth_password='goodboySeth',
            )
            return HttpResponseRedirect(reverse('vrpages:send_email'))
    return render(request, 'vrpages/send_email.html', {'form': form})
