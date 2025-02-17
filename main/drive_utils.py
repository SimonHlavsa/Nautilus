import os
import re
import requests
from django.core.cache import cache
import datetime

def get_folders(folder_id, refresh=False):
    """
    Retrieves a list of all folders within a specified folder on Google Drive,
    utilizing cache for optimization.

    This method first checks if the data is available in the cache. If not, it 
    fetches the data from the Google Drive API and stores it in the cache for 
    future use.

    :param folder_id: The ID of the parent folder in Google Drive.
    :return: A list of folders in the specified folder, or an empty list if the 
             API request fails.
    """
    cache_key = f"folders_{folder_id}"
    
    if not refresh:
        folders = cache.get(cache_key)
        if folders is not None:
            return folders

    url = "https://www.googleapis.com/drive/v3/files"
    params = {
        "q": f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false",
        "fields": "files(id, name)",
        "key": os.environ.get('GOOGLE_API_KEY')
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        folders = response.json().get("files", [])
        cache.set(cache_key, folders, 600)
        return folders
    else:
        print(f"Chyba: {response.status_code}, {response.text}")
        return []


def get_images_in_folder(folder_id, refresh=False):
    """
    Retrieves all images within a specific folder on Google Drive, utilizing 
    cache for optimization.

    This method checks the cache for pre-fetched data. If the data is not 
    available, it fetches the list of images from the Google Drive API and 
    stores it in the cache for future use.

    :param folder_id: The ID of the folder in Google Drive.
    :return: A list of images in the specified folder, or an empty list if the 
             API request fails.
    """
    cache_key = f"images_in_{folder_id}"

    if not refresh:
        images = cache.get(cache_key)
        if images is not None:
            return images

    url = "https://www.googleapis.com/drive/v3/files"
    query = f"'{folder_id}' in parents and mimeType contains 'image/' and trashed=false"
    params = {
        "q": query,
        "fields": "files(id, name, parents, thumbnailLink)",
        "key": os.environ.get('GOOGLE_API_KEY')
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        images = response.json().get("files", [])
        cache.set(cache_key, images, 600)
        return images
    else:
        print(f"Chyba: {response.status_code}, {response.text}")
        return []
    

def get_future_calendar_events(calendar_id, refresh=False):
    """
    Fetches all future events from a public Google Calendar using caching.

    :param calendar_id: Calendar ID (e.g., an email address or a special calendar ID)
    :param refresh: If set to True, forces a refresh of data from the API
    :return: A list of future events, or an empty list in case of an error.
    """
    cache_key = f"future_calendar_events_{calendar_id}"
    
    if not refresh:
        events = cache.get(cache_key)
        if events is not None:
            return events

    url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"
    params = {
        "key": os.environ.get('GOOGLE_API_KEY'),
        "timeMin": datetime.datetime.utcnow().isoformat() + "Z",  # only future events
        "singleEvents": True,
        "orderBy": "startTime",
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        events = response.json().get("items", [])
        cache.set(cache_key, events, 3)  # Cache for 10 mins
        return events
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []


def extract_fb_link(description):
    """
    Extracts a Facebook link from the event description if it appears at the beginning as an HTML link
    or as plain text. If a link is found, it is removed from the description.
    
    Returns a tuple (fb_link, new_description).
    """
    if not description:
        return "", description

    # First, try to find an HTML link at the beginning of the text (optionally preceded by <br> tags)
    pattern = r'^\s*(?:<br\s*/?>\s*)*<a\s+href="([^"]+)"[^>]*>.*?</a>\s*(?:<br\s*/?>)?'
    match = re.search(pattern, description, flags=re.IGNORECASE | re.DOTALL)
    if match:
        fb_link = match.group(1)
        new_description = description[match.end():].strip()
        return fb_link, new_description
    else:
        # If no HTML link is found, split the text by <br>
        parts = description.split("<br>")
        first_line = parts[0].strip()
        # Regular expression to detect a URL in the first line
        url_pattern = r"(https?://\S+|www\.\S+|fb\.me/\S+)"
        match_line = re.search(url_pattern, first_line)
        if match_line:
            fb_link = match_line.group(0)
            new_description = "<br>".join(parts[1:]).strip() if len(parts) > 1 else ""
            return fb_link, new_description
        else:
            return "", description