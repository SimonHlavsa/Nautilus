from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.template.loader import render_to_string
from .forms import RegistrationForm

def homepage(request):
    return render(request, 'main/base.html')

def calendar(request):
    # Here you can load events via API and send them to the template
    events = []  # Currently an empty list
    return render(request, 'main/calendar.html', {'events': events})

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Retrieve form data
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            certification_level = form.cleaned_data['certification_level']
            certification_proof_files = form.cleaned_data['certification_proof_files']

            # Prepare email details
            email_subject = 'New Registration'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = ['simon.hlavsa55@gmail.com']

            # Prepare plain text content
            text_content = f"""
First Name: {first_name}
Last Name: {last_name}
Email: {email}
Phone: {phone}
Certification Level: {certification_level}
"""

            # Render the HTML content from the template
            html_content = render_to_string('emails/registration_email.html', {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': phone,
                'certification_level': certification_level,
            })

            # Create the email message
            email_message = EmailMultiAlternatives(
                subject=email_subject,
                body=text_content,
                from_email=from_email,
                to=to_email
            )

            # Attach the HTML version
            email_message.attach_alternative(html_content, "text/html")

            # Attach files
            for file in certification_proof_files:
                email_message.attach(file.name, file.read(), file.content_type)

            # Send the email
            email_message.send()

            return render(request, 'main/form_success.html')
        else:
            return render(request, 'main/form.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'main/form.html', {'form': form})

def gallery(request):
    return render(request, 'main/gallery.html')

def contacts(request):
    return render(request, 'main/contacts.html')