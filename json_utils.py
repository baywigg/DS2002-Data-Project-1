import requests

def get_json(asset, interval):
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.get(url=f"https://api.coincap.io/v2/assets/{asset}/history?interval={interval}", headers=headers)
    except Exception as e:
        return []
    
    return response.json() if response.status_code == 200 else []