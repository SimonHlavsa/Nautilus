from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
# from .forms import RegistrationForm

def homepage(request):
    return render(request, 'main/homepage.html')

def contacts(request):
    return render(request, 'main/contacts.html')

def gallery(request):
    return render(request, 'main/gallery.html')

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Send an email with the form data
            send_mail(
                'New registration for the club',
                f"Name: {form.cleaned_data['name']}\nEmail: {form.cleaned_data['email']}",
                'from@example.com',  # Sender (set your own)
                ['to@example.com'],  # Recipient (e.g., the club's email)
            )
            return HttpResponse('Thank you for registering!')
    else:
        form = RegistrationForm()

    return render(request, 'main/registration.html', {'form': form})


def calendar(request):
    # Here you can load events via API and send them to the template
    events = []  # Currently an empty list
    return render(request, 'main/calendar.html', {'events': events})
