import requests

def get_json(asset, interval):
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.get(url=f"https://api.coincap.io/v2/assets/{asset}/history?interval={interval}", headers=headers)
    except Exception as e:
        return []
    
    return response.json() if response.status_code == 200 else []

def get_price_and_time_change(df):
    price_changes = [0]
    time_changes = [0]
    for i, row in df.iterrows():
        if i == 0:
            continue
        
        prev_price = df.at[i - 1, "priceUsd"]
        cur_price = row["priceUsd"]

        prev_time = df.at[i-1, "time"]
        cur_time = row["time"]

        price_changes.append(float(cur_price) - float(prev_price))
        time_changes.append(int(cur_time) - int(prev_time))
    
    return price_changes, time_changes