import pandas as pd
import requests
import json

base_url = "https://api.weather.gov/"


def get_weather(base_url, lat, lon, date, time):
    base_url = base_url

    day_filter = date
    time_filter = time

    geo_data = pd.json_normalize(
        json.loads(requests.get(base_url + "points/{},{}".format(lat, lon)).text)
    )["properties.forecastHourly"][0]

    grid_data = pd.json_normalize(json.loads(requests.get(geo_data).text))[
        "properties.periods"
    ][0]

    hourly_forecast_table = pd.json_normalize(grid_data)

    hourly_forecast_table["date"] = pd.to_datetime(
        hourly_forecast_table["startTime"]
    ).dt.date.astype(str)
    hourly_forecast_table["time"] = pd.to_datetime(
        hourly_forecast_table["startTime"]
    ).dt.time.astype(str)

    date_forecast = hourly_forecast_table[hourly_forecast_table["date"] == day_filter]
    hour_forecast = date_forecast[date_forecast["time"] == time_filter]

    columns_to_keep = [
        "date",
        "time",
        "isDaytime",
        "shortForecast",
        "temperature",
        "temperatureUnit",
        "windSpeed",
        "windDirection",
        "probabilityOfPrecipitation.value",
        "dewpoint.value",
        "relativeHumidity.value",
    ]
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
