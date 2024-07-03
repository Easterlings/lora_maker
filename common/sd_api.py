

import json
import requests
from config.stablediffusion_api import IMG2IMG_PARAMETERS
from config.system import SD_API


def _request(url, data=None, method="GET", headers=None):
    if headers is None:
        headers = {
            "Content-Type": "application/json",
            "Accept-Encoding": "identity",
        }
    if method.upper() == "POST":
        response = requests.post(url, data=json.dumps(data), headers=headers)
    elif method.upper() == "GET":
        response = requests.get(url, params=data, headers=headers)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 422:
        raise Exception(f"Validation Error:: {response.json()}")
    else:
        raise Exception(f"Error: {response.status_code} {response.text}")

def img2img_request(data):
    api_url = SD_API
    url = f"{api_url}/sdapi/v1/img2img"
    return _request(url, data, "POST")

def get_img2img_request_data(select="default"):
    data = dict(IMG2IMG_PARAMETERS[select]) #加dict解决缓存问题
    # for key in safe_img2img_params:
    #     if key in parameter:
    #         data[key] = parameter[key]

    return data