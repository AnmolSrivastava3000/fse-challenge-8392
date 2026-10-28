from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import pandas as pd
from datetime import datetime
import asyncio

app = FastAPI(title="Wind Generation Analysis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ACTUALS_URL = "https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELHH/stream"
FORECASTS_URL = "https://data.elexon.co.uk/bmrs/api/v1/datasets/WINDFOR/stream"

async def fetch_data(client, url, params):
    response = await client.get(url, params=params, headers={"Accept": "application/json"})
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail=f"Failed to fetch data from {url}: {response.text}")
    return response.json()

@app.get("/api/analysis")
async def get_wind_analysis():
    # Using the exact parameter names from the Elexon documentation.
    # Restricting to a 7-day window to prevent API timeouts on the /stream endpoint.
    actuals_params = {
        "settlementDateFrom": "2024-01-02",
        "settlementDateTo": "2024-01-09",
        "fuelType": "WIND"
    }
    forecast_params = {
        "publishDateTimeFrom": "2024-01-01T00:00:00Z",
        "publishDateTimeTo": "2024-01-09T23:59:59Z"
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        actuals_task = fetch_data(client, ACTUALS_URL, actuals_params)
        forecasts_task = fetch_data(client, FORECASTS_URL, forecast_params)
        
        actuals_data, forecasts_data = await asyncio.gather(actuals_task, forecasts_task)

    # 1. Process Actuals
    df_actual = pd.DataFrame(actuals_data)
    if df_actual.empty:
        raise HTTPException(status_code=404, detail="No actuals data found for the date range.")
        
    df_actual['startTime'] = pd.to_datetime(df_actual['startTime'])
    df_actual = df_actual[['startTime', 'generation']].rename(columns={'generation': 'actual_generation'})

    # 2. Process Forecasts
    df_forecast = pd.DataFrame(forecasts_data)
    if df_forecast.empty:
        raise HTTPException(status_code=404, detail="No forecast data found for the date range.")

    df_forecast['startTime'] = pd.to_datetime(df_forecast['startTime'])
    df_forecast['publishTime'] = pd.to_datetime(df_forecast['publishTime'])
    df_forecast = df_forecast.rename(columns={'generation': 'forecast_generation'})

    # 3. Day-Ahead Filtering
    df_forecast['delivery_date'] = df_forecast['startTime'].dt.date
    df_forecast['decision_date'] = df_forecast['delivery_date'] - pd.Timedelta(days=1)
    
    df_forecast['publish_date'] = df_forecast['publishTime'].dt.date
    day_ahead_forecasts = df_forecast[df_forecast['publish_date'] <= df_forecast['decision_date']]
    
    day_ahead_forecasts = day_ahead_forecasts.sort_values('publishTime', ascending=False)
    day_ahead_forecasts = day_ahead_forecasts.drop_duplicates(subset=['startTime'])

    # 4. Merge and Calculate
    merged = pd.merge(df_actual, day_ahead_forecasts[['startTime', 'forecast_generation', 'publishTime']], on='startTime')
    
    if merged.empty:
        raise HTTPException(status_code=404, detail="Data fetched successfully, but no matching day-ahead records found.")
        
    merged = merged.sort_values('startTime')
    merged['error_mw'] = merged['actual_generation'] - merged['forecast_generation']
    merged['absolute_error_mw'] = merged['error_mw'].abs()
    
    merged['startTime'] = merged['startTime'].dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    merged['publishTime'] = merged['publishTime'].dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    mae = float(merged['absolute_error_mw'].mean())
    rmse = float((merged['error_mw'] ** 2).mean() ** 0.5)
    
    return {
        "metrics": {
            "mean_absolute_error_mw": round(mae, 2),
            "root_mean_square_error_mw": round(rmse, 2),
            "total_settlement_periods": len(merged)
        },
        "time_series": merged.to_dict(orient="records")
    }