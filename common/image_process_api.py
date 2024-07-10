
import requests
from config.system import IMAGE_PROCESS_API_URL

def rem_bg_request(file):
    url = f"{IMAGE_PROCESS_API_URL}/api/rem_bg"
    return requests.post(url, files={'image': file})