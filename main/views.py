from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegistrationForm

def homepage(request):
    return render(request, 'main/base.html')

def contacts(request):
    return render(request, 'main/contacts.html')

def gallery(request):
    return render(request, 'main/gallery.html')

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Process email sending
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            send_mail(
                'New Registration',  # Email subject
                f"First Name: {first_name}\nLast Name: {last_name}\nEmail: {email}",  # Email content
                settings.DEFAULT_FROM_EMAIL,  # Sender (set your own)
                ['simon.hlavsa55@gmail.com'],  # Recipient
            )

            return render(request, 'main/form_success.html')  # Display success page after form submission
    else:
        form = RegistrationForm()

    return render(request, 'main/form.html', {'form': form})  # Render form template with the form object

def calendar(request):
    # Here you can load events via API and send them to the template
    events = []  # Currently an empty list
    return render(request, 'main/calendar.html', {'events': events})
