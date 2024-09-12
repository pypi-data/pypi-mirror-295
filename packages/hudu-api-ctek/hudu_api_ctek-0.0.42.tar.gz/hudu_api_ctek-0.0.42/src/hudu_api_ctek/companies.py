import requests

def get_companies_all(api_baseurl, api_key):
    page = 1
    headers = {'x-api-key': api_key}
    all_companies = []
    page_size = 100

    while True:
        url = f'{api_baseurl}/companies?page={page}&page_size={page_size}'
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            companies = data.get('companies', [])
            if not companies:
                break
            
            all_companies.extend(companies)

            if len(companies) < page_size:
                break
            
            page += 1
        
        except requests.exceptions.RequestException as e:
            return {"companies": []}, f"Error fetching companies: {e}"
    
    return all_companies, None
