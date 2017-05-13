import datetime

from django.core.mail import send_mail
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView

from . import forms
from . import models
from .resources import PolishedUrlResource

# Create your views here.
def vrpages_list(request):
    vrpages = models.VRPage.objects.all()
    return render(request, 'vrpages/vrpages_list.html', {'vrpages': vrpages})

def vrpage_detail(request, pk):
    vrpage = get_object_or_404(models.VRPage, pk=pk)
    return render(request, 'vrpages/vrpage_detail.html', {'vrpage': vrpage})


class VRPageCreateView(CreateView):
    fields = ("vrpage_name",
              "email_address",
              "email_username",
              "email_username",
              "email_password",
              "email_server",
              "email_from_name"
    )
    model = models.VRPage


class VRPageUpdateView(UpdateView):
    fields = ("vrpage_name",
              "email_address",
              "email_username",
              "email_username",
              "email_password",
              "email_server",
              "email_from_name"
    )
    model = models.VRPage


class VRPageDeleteView(DeleteView):
    model = models.VRPage
    success_url = reverse_lazy('vrpages:vrpages_list')


def 


def templates_list(request):
    templates = models.MessageTemplate.objects.all()
    return render(request, 'vrpages/templates_list.html', {'templates': templates})

def template_detail(request, pk):
    template = get_object_or_404(models.MessageTemplate, pk=pk)
    return render(request, 'vrpages/template_detail.html', {'template': template})


class MessageTemplateCreateView(CreateView):
    fields = ("vrpage",
              "template_type",
              "subject",
              "message_body"
    )
    model = models.MessageTemplate


class MessageTemplateUpdateView(UpdateView):
    fields = ("vrpage",
              "template_type",
              "subject",
              "message_body"
    )
    model = models.MessageTemplate


class MessageTemplateDeleteView(DeleteView):
    model = models.MessageTemplate
    success_url = reverse_lazy('vrpages:templates_list')


def messages_list(request):
    messages = models.MessageTemplate.objects.all()
    return render(request, 'vrpages/messages_list.html', {'messages': messages})

def unsubscribes_list(request):
    unsubscribes = models.Unsubscribed.objects.all()
    return render(request, 'vrpages/unsubscribes_list.html', {'unsubscribes': unsubscribes})

def unsubscribe_from_vrpage(request):
    form = forms.UnsubscribeFromVRPageForm()
    if request.method == 'POST':
        form = forms.UnsubscribeFromVRPageForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            vrpage = form.cleaned_data['vrpage']
            polished_url = models.PolishedUrl.objects.get(polished_email=email, vrpage=vrpage)
            polished_url.unsubscribe_from_vrpage = True
            polished_url.save()
            form.save()
            return HttpResponseRedirect(reverse('vrpages:unsubscribes_list'))
    return render(request, 'vrpages/unsubscribe_from_vrpage_form.html', {'form': form})

def unsubscribe_permanently(request):
    form = forms.UnsubscribePermanentlyForm()
    if request.method == 'POST':
        form = forms.UnsubscribePermanentlyForm(request.POST)
        if form.is_valid():
            email_input = form.cleaned_data['email']
            models.PolishedUrl.objects.filter(polished_email=email_input).update(unsubscribe_permanently=True)
            email = form.save(commit=False)
            email.permanent = True
            email.save()
            return HttpResponseRedirect(reverse('vrpages:unsubscribes_list'))
    return render(request, 'vrpages/unsubscribe_permanently_form.html', {'form': form})

def unsubscribe_entire_domain(request):
    form = forms.UnsubscribeEntireDomainForm()
    if request.method == 'POST':
        form = forms.UnsubscribeEntireDomainForm(request.POST)
        if form.is_valid():
            domain_input = form.cleaned_data['domain']
            polished_urls = models.PolishedUrl.objects.all()
            for polished_url in polished_urls:
                if domain_input in polished_url.polished_email:
                    polished_url.unsubscribe_permanently = True
                    polished_url.save()
            domain = form.save(commit=False)
            domain.entire_domain = True
            domain.save()
            return HttpResponseRedirect(reverse('vrpages:unsubscribes_list'))
    return render(request, 'vrpages/unsubscribe_entire_domain_form.html', {'form': form})

def no_email(request, pk):
    vrpage = get_object_or_404(models.VRPage, pk=pk)
    return render(request, 'vrpages/no_email.html', {'vrpage': vrpage})

def send_email(request, pk, template_type):
    vrpage = models.VRPage.objects.get(pk=pk)
    message_template = models.MessageTemplate.objects.get(vrpage_id=pk, template_type=template_type)
    if template_type == 'First':
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
                    email_message.message_type = 'First'
                    email_message.polished_url = polished_url
                    email_message.save()
                    return HttpResponseRedirect(reverse('vrpages:send_email', args=[pk, template_type]))
            return render(request, 'vrpages/send_email.html', {'form': form})
    elif template_type == 'Second':
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
                        email_message.message_type = 'Second'
                        email_message.polished_url = polished_url
                        email_message.save()
                        return HttpResponseRedirect(reverse('vrpages:send_email', args=[pk, template_type]))
                return render(request, 'vrpages/send_email.html', {'form': form})
            return HttpResponseRedirect(reverse('vrpages:no_email', args=[pk]))

