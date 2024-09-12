import requests

def get_assets_by_layout_id(api_baseurl, api_key, asset_layout_id):
    page = 1
    headers = {'x-api-key': api_key}
    all_assets = []
    page_size = 100  # Adjust as needed

    while True:
        url = f'{api_baseurl}/assets?asset_layout_id={asset_layout_id}&page={page}&page_size={page_size}'
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = response.json()
            
            assets = data.get('assets', [])
            if not assets:  # If no assets are returned, break the loop
                break
            
            all_assets.extend(assets)

            # If fewer assets are returned than per_page, it's the last page
            if len(assets) < page_size:
                break
            
            page += 1
        
        except requests.exceptions.RequestException as e:
            return {"assets": []}, f"Error fetching assets: {e}"
    
    return all_assets, None
