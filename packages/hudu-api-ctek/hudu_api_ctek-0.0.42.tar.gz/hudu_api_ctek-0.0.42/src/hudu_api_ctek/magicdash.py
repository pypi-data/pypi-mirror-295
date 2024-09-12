import requests
import logging

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def create_magic_dash(api_baseurl, api_key, dash_name, dash_message, dash_shade, dash_content, company_name):
    try:
        url = f"{api_baseurl}/magic_dash"
        payload = {
            "title": f"{dash_name}",
            "message": f"{dash_message}",
            "shade": f"{dash_shade}",
            "content": f"{dash_content}",
            "content_link": "",
            "image_url": "",
            "icon": "fas fa-network-wired",
            "company_name": company_name
        }
        print(f"Creating magic dash: {payload}")
        logger.info(f"Creating magic dash: {payload}")
        headers = {"x-api-key": api_key}
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, f"Error creating magic dash: {e}"