import datetime

from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from . import forms
from . import models

# Create your views here.
def vrpages_list(request):
    vrpages = models.VRPage.objects.all()
    return render(request, 'vrpages/vrpages_list.html', {'vrpages': vrpages})

def messages_list(request):
    messages = models.MessageTemplate.objects.all()
    return render(request, 'vrpages/messages_list.html', {'messages': messages})

def no_email(request, pk):
    vrpage = get_object_or_404(models.VRPage, pk=pk)
    return render(request, 'vrpages/no_email.html', {'vrpage': vrpage})

def send_email(request, pk, template_type):
    vrpage = models.VRPage.objects.get(pk=pk)
    message_template = models.MessageTemplate.objects.get(vrpage_id=pk, template_type=template_type)
    if template_type == 'first':
        try:
            polished_url = models.PolishedUrl.objects.filter(vrpage_id=pk, first_message_sent=False)[0]
        except IndexError:
            return HttpResponseRedirect(reverse('vrpages:no_email', args=[pk]))
        else:
            message_variables = {'contactname': polished_url.contact_name,
                                 'url': polished_url.polished_url,
                                 'anchortext': polished_url.anchor_text,
                                 'pagetitle': polished_url.page_title
                                 }
            message_subject = message_template.subject.format(**message_variables)
            message_body = message_template.message_body.format(**message_variables)
            form = forms.SendEmailForm(initial={'email': polished_url.polished_email,
                                                'subject': message_subject,
                                                'message_body': message_body})
            if request.method == 'POST':
                form = forms.SendEmailForm(request.POST)
                if form.is_valid():
                    send_mail(
                        form.cleaned_data['subject'],
                        form.cleaned_data['message_body'],
                        '{} <{}>'.format(vrpage.email_from_name, vrpage.email_address),
                        [form.cleaned_data['email']],
                        fail_silently=False,
                        auth_user=vrpage.email_address,
                        auth_password=vrpage.email_password
                    )
                    polished_url.first_message_sent = True
                    polished_url.save()
                    email_message = form.save(commit=False)
                    email_message.message_type = 'first'
                    email_message.polished_url = polished_url
                    email_message.save()
                    return HttpResponseRedirect(reverse('vrpages:send_email', args=[pk, template_type]))
            return render(request, 'vrpages/send_email.html', {'form': form})
    elif template_type == 'second':
        try:
            polished_url = models.PolishedUrl.objects.filter(vrpage_id=pk,
                                                            first_message_sent=True,
                                                            second_message_sent=False)[0]
        except IndexError:
            return HttpResponseRedirect(reverse('vrpages:no_email', args=[pk]))
        else:
            first_message = models.EmailMessage.objects.get(polished_url=polished_url)
            first_message_sent_date = first_message.created_at
            now = timezone.now()
            gap = now - first_message_sent_date
            if gap >= datetime.timedelta(minutes=10):
                message_variables = {'contactname': polished_url.contact_name,
                                 'url': polished_url.polished_url,
                                 'anchortext': polished_url.anchor_text,
                                 'pagetitle': polished_url.page_title
                                 }
                message_subject = message_template.subject.format(**message_variables)
                message_body = message_template.message_body.format(**message_variables)
                message_body += "\n\n" + "=" * 8 + " Forwarded message " + "=" * 8 + "\n"
                message_body += "From: {}\n".format(vrpage.email_address)
                message_body += "Date: {}\n".format(first_message.created_at.strftime('%A, %m/%d/%y at %I:%M %p'))
                message_body += "Subject: {}\n".format(first_message.subject)
                message_body += "To: {}\n\n".format(first_message.email)
                message_body += first_message.message_body
                form = forms.SendEmailForm(initial={'email': polished_url.polished_email,
                                                    'subject': message_subject,
                                                    'message_body': message_body})
                if request.method == 'POST':
                    form = forms.SendEmailForm(request.POST)
                    if form.is_valid():
                        send_mail(
                            form.cleaned_data['subject'],
                            form.cleaned_data['message_body'],
                            '{} <{}>'.format(vrpage.email_from_name, vrpage.email_address),
                            [form.cleaned_data['email']],
                            fail_silently=False,
                            auth_user=vrpage.email_address,
                            auth_password=vrpage.email_password
                        )
                        polished_url.second_message_sent = True
                        polished_url.save()
                        email_message = form.save(commit=False)
                        email_message.message_type = 'second'
                        email_message.polished_url = polished_url
                        email_message.save()
                        return HttpResponseRedirect(reverse('vrpages:send_email', args=[pk, template_type]))
                return render(request, 'vrpages/send_email.html', {'form': form})
            return HttpResponseRedirect(reverse('vrpages:no_email', args=[pk]))

