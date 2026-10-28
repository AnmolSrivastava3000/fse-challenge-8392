import requests
import json

# Actual generation endpoint
ACTUALS_URL = "https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELHH/stream"
# Forecast generation endpoint
FORECASTS_URL = "https://data.elexon.co.uk/bmrs/api/v1/datasets/WINDFOR/stream"

def test_actuals():
    print("Fetching Actuals (FUELHH) for Jan 1, 2026...")
    # Elexon typically uses 'from' and 'to' or 'startTime' parameters in ISO 8601 format
    params = {
        "publishTimeFrom": "2026-01-01T00:00:00Z",
        "publishTimeTo": "2026-01-01T23:59:59Z"
    }
    headers = {"Accept": "application/json"}
    
    response = requests.get(ACTUALS_URL, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        # Filter to see just the WIND data as requested by PM
        wind_data = [item for item in data if item.get('fuelType') == 'WIND']
        print(f"Success! Found {len(wind_data)} WIND records.")
        if wind_data:
            print("Sample Record:", json.dumps(wind_data[0], indent=2))
    else:
        print(f"Failed to fetch actuals. Status code: {response.status_code}")
        print("Response:", response.text)

def test_forecasts():
    print("\nFetching Forecasts (WINDFOR) for Jan 1, 2026...")
    params = {
        "publishTimeFrom": "2026-01-01T00:00:00Z",
        "publishTimeTo": "2026-01-01T23:59:59Z"
    }
    headers = {"Accept": "application/json"}
    
    response = requests.get(FORECASTS_URL, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"Success! Fetched {len(data)} forecast records.")
        if data:
             print("Sample Record:", json.dumps(data[0], indent=2))
    else:
        print(f"Failed to fetch forecasts. Status code: {response.status_code}")
        print("Response:", response.text)

if __name__ == "__main__":
    test_actuals()
    test_forecasts()