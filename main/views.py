import os
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from main.drive_utils import extract_fb_link, get_folders, get_future_calendar_events, get_images_in_folder
from main.forms import RegistrationForm

def homepage(request):
    """
    Renders the homepage view.
    
    This view returns the homepage template, providing the basic introduction 
    to the site.
    """
    return render(request, 'main/home.html')

def calendar(request):
    """
    Renders the main/calendar.html template and passes Google Calendar event data to it.
    """
    calendar_id = "vsenautilus@gmail.com"
    events = get_future_calendar_events(calendar_id)
    
    # Process each event's description to extract the Facebook link, if present
    for event in events:
        if event.get("description"):
            fb_link, new_description = extract_fb_link(event["description"])
            if fb_link:
                event["fbLink"] = fb_link
                event["description"] = new_description
            else:
                event["fbLink"] = ""
        else:
            event["fbLink"] = ""
    
    context = {
        "events": events,
    }
    
    return render(request, "main/calendar.html", context)

def registration(request):
    """
    Handles the registration form submission and email notification.

    If the request is a POST, it validates the submitted data, retrieves it, 
    and sends a notification email. If the form is not valid, it re-renders 
    the registration form with validation errors. For GET requests, it 
    displays an empty registration form.
    """
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
            return render(request, 'main/registration.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'main/registration.html', {'form': form})

def gallery(request):
    """
    Displays the gallery view with folders and their thumbnails.

    This view retrieves folders from Google Drive and, for each folder, fetches
    images to display the first image as a thumbnail. The results are cached 
    for optimization.
    """

    root_folder_id = os.environ.get('GOOGLE_FOLDER_ID')
    folders = get_folders(root_folder_id)
    enhanced_folders = []

    for folder in folders:
        images = get_images_in_folder(folder['id'])
        if not images:
            continue

        first_image = images[0] if images else None
        thumbnail_link = first_image.get('thumbnailLink') if first_image else None
        high_res_link = thumbnail_link.replace("s220", "s800")
        enhanced_folders.append({
            'id': folder['id'],
            'name': folder['name'],
            'thumbnailLink': high_res_link 
        })
        
    return render(request, 'main/gallery.html', {'folders': enhanced_folders})

def gallery_detail(request):
    """
    Displays all images within a selected folder on Google Drive.

    This view retrieves images from the specified folder using cache or API 
    and renders them in the gallery detail template.
    """
    folder_id = request.GET.get('folder_id')
    folder_name = request.GET.get('folder_name', 'Gallery')

    images = get_images_in_folder(folder_id)
    enhanced_folders = []

    for img in images:
        thumbnail_link = img.get('thumbnailLink') if img else None
        high_res_link = thumbnail_link.replace("s220", "s800")
        enhanced_folders.append({
            'name': img['name'],
            'high_res_link': high_res_link,
        })

    return render(request, 'main/gallery_detail.html', {'images': enhanced_folders, 'folder_name': folder_name})

def contacts(request):
    """
    Renders the contacts view.

    This view displays contact information and related resources for the site.
    """
    return render(request, 'main/contacts.html')

@require_http_methods(["HEAD", "GET"])
def ping(request):
    return HttpResponse("pong")