import requests
import pandas as pd

# Fetch HDFC Top 100 Direct NAV
url = 'https://api.mfapi.in/mf/125497'
data = requests.get(url).json()
df = pd.DataFrame(data['data'])
df.to_csv('data/raw/125497_HDFC.csv', index=False)
print("Saved HDFC Top 100 Direct")

# Fetch 5 key schemes
schemes = {
    '119551': 'SBI_Bluechip',
    '120503': 'ICICI_Bluechip',
    '118632': 'Nippon_Large_Cap',
    '119092': 'Axis_Bluechip',
    '120841': 'Kotak_Bluechip'
}

for code, name in schemes.items():
    url = f'https://api.mfapi.in/mf/{code}'
    data = requests.get(url).json()
    df = pd.DataFrame(data['data'])
    df.to_csv(f'data/raw/{code}_{name}.csv', index=False)
    print(f"Saved {name}")
