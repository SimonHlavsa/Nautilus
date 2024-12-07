import os
import requests
from django.core.cache import cache

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
        cache.set(cache_key, folders, 3600)
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
        cache.set(cache_key, images, 3600)
        return images
    else:
        print(f"Chyba: {response.status_code}, {response.text}")
        return []