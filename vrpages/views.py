from django.shortcuts import render

# Create your views here.
def send_email(request):
    return render(request, 'vrpages/send_email.html')
