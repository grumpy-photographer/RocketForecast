# %%
import pandas as pd
import requests
import json

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

# %%
base_url = "https://api.weather.gov/"

# %% [markdown]
# ***


# %%
def get_weather(base_url, lat, lon, date, time):
    day_filter = date
    time_filter = time

    geo_data = pd.json_normalize(
        json.loads(
            requests.get(
                base_url + "points/{},{}".format(lat, lon)
                ).text
            )
        )['properties.forecastHourly'][0]
    
    grid_data = pd.json_normalize(
        json.loads(
            requests.get(
                geo_data
                ).text
            )
        )['properties.periods'][0]
    
    hourly_forecast_table = pd.json_normalize(grid_data)

    hourly_forecast_table['date'] = pd.to_datetime(hourly_forecast_table['startTime']).dt.date.astype(str)
    hourly_forecast_table['time'] = pd.to_datetime(hourly_forecast_table['startTime']).dt.time.astype(str)

    date_forecast = hourly_forecast_table[hourly_forecast_table['date'] == day_filter]
    hour_forecast = date_forecast[date_forecast['time'] == time_filter]

    columns_to_keep = ['date', 'time', 'isDaytime', 'shortForecast', 'temperature', 'temperatureUnit', 'windSpeed', 'windDirection', 'probabilityOfPrecipitation.value', 'dewpoint.value', 'relativeHumidity.value']
    forecast = hour_forecast[columns_to_keep]

    forecast = forecast.rename(
        columns={
            "shortForecast": "Forecast",
            "probabilityOfPrecipitation.value": "Chance of Precipitation",
            "dewpoint.value": "Dewpoint",
            "relativeHumidity.value": "Humidity",
        }
    )
    
    return forecast


# %% [markdown]
# ***

# %% [markdown]
# Cape Canaveral, FL, USA

# %%
# Starlink Group 6-11
# get_weather(base_url, 28.561941, -80.577357, '2023-08-23', '00:00:00')

# %%
# Starlink Group 7-1
# get_weather(base_url, 28.561941, -80.577357, '2023-08-22', '06:00:00')
