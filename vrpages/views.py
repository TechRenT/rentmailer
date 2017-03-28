from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import forms

# Create your views here.
def send_email(request):
    form = forms.SendEmailForm()
    if request.method == 'POST':
        form = forms.SendEmailForm(request.POST)
        if form.is_valid():
            send_mail(
                'Suggestion from {}'.format(form.cleaned_data['name']),
                form.cleaned_data['message'],
                '{} <{}>'.format('Renelle Tigue', 'purpose.renelle@gmail.com'),
                [form.cleaned_data['email']],
                fail_silently=False,
                auth_user='purpose.renelle@gmail.com',
                auth_password='goodboySeth',
            )
            return HttpResponseRedirect(reverse('vrpages:send_email'))
    return render(request, 'vrpages/send_email.html', {'form': form})
