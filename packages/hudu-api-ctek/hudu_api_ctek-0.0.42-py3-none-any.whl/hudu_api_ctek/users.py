import requests

def get_users(api_baseurl, api_key):
    headers = {'x-api-key': api_key}
    page_size = 100
    url = f'{api_baseurl}/users?page_size={page_size}'
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        users = data.get('users', [])
    
    except requests.exceptions.RequestException as e:
        return {"users": []}, f"Error fetching users: {e}"
    
    return users, None
