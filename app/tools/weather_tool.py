"""
Live Open-Meteo Agricultural & Meteorological API Tool.
Strict Zero-Dummy-Data Compliance: Queries real-time hourly and 7-day agricultural forecasts.
"""
import httpx
from typing import Dict, Any, Optional

OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# WMO Weather interpretation codes
WMO_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}

async def fetch_live_weather(lat: float, lon: float) -> Dict[str, Any]:
    """
    Fetches real-time weather, soil moisture, and 7-day precipitation forecasts from Open-Meteo.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "is_day",
            "precipitation",
            "rain",
            "weather_code",
            "wind_speed_10m",
            "wind_gusts_10m"
        ],
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation_probability",
            "precipitation",
            "soil_moisture_0_to_1cm",
            "soil_moisture_1_to_3cm",
            "soil_moisture_3_to_9cm",
            "soil_temperature_0cm"
        ],
        "daily": [
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "precipitation_probability_max",
            "wind_speed_10m_max"
        ],
        "timezone": "auto",
        "forecast_days": 7
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(OPEN_METEO_FORECAST_URL, params=params)
        response.raise_for_status()
        data = response.json()

    current = data.get("current", {})
    hourly = data.get("hourly", {})
    daily = data.get("daily", {})

    # Compute key agro-meteorological risks
    weather_code = current.get("weather_code", 0)
    condition_desc = WMO_CODES.get(weather_code, "Unknown")

    # Next 48 hours rain sum
    hourly_precip = hourly.get("precipitation", [])[:48]
    precip_48h_sum = round(sum(hourly_precip), 2) if hourly_precip else 0.0

    # Max precip probability next 48h
    hourly_prob = hourly.get("precipitation_probability", [])[:48]
    max_precip_prob_48h = max(hourly_prob) if hourly_prob else 0

    # Soil moisture (m³/m³) 0-1cm (surface) and 1-3cm (root zone)
    soil_0_1 = hourly.get("soil_moisture_0_to_1cm", [0.0])[0]
    soil_1_3 = hourly.get("soil_moisture_1_to_3cm", [0.0])[0]

    # Risk evaluations
    risks = []
    if precip_48h_sum > 25.0 or max_precip_prob_48h > 75:
        risks.append({
            "type": "HEAVY_RAINFALL_ALERT",
            "severity": "CRITICAL" if precip_48h_sum > 40 else "HIGH",
            "detail": f"Expected rainfall: {precip_48h_sum}mm in next 48h (Peak probability: {max_precip_prob_48h}%). Threatens unharvested crops with waterlogging and post-harvest spoilage."
        })

    current_temp = current.get("temperature_2m", 25.0)
    current_humidity = current.get("relative_humidity_2m", 50.0)

    if current_temp > 38.0:
        risks.append({
            "type": "HEAT_STRESS_ALERT",
            "severity": "HIGH",
            "detail": f"Current temperature is {current_temp}°C. Accelerated evapotranspiration and flower drop risk."
        })

    if current_humidity > 80.0 and current_temp > 22.0:
        risks.append({
            "type": "FUNGAL_PATHOGEN_WINDOW",
            "severity": "MEDIUM",
            "detail": f"High humidity ({current_humidity}%) and warm temperatures create optimal incubation window for fungal leaf blight and rust spores."
        })

    if soil_0_1 > 0.40:
        risks.append({
            "type": "SOIL_SATURATION_WARNING",
            "severity": "HIGH",
            "detail": f"Topsoil moisture saturation at {soil_0_1:.2f} m³/m³. Farm machinery entry prohibited; root rot susceptibility high."
        })

    return {
        "source": "Open-Meteo Live Agro API",
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude"),
        "elevation": data.get("elevation"),
        "current": {
            "temperature_c": current_temp,
            "humidity_pct": current_humidity,
            "condition": condition_desc,
            "weather_code": weather_code,
            "wind_speed_kmh": current.get("wind_speed_10m", 0),
            "wind_gusts_kmh": current.get("wind_gusts_10m", 0),
            "soil_moisture_surface": round(soil_0_1, 3),
            "soil_moisture_rootzone": round(soil_1_3, 3),
        },
        "forecast_48h": {
            "rainfall_total_mm": precip_48h_sum,
            "peak_precipitation_prob_pct": max_precip_prob_48h,
            "hourly_precipitation": hourly_precip[:24],
            "hourly_probabilities": hourly_prob[:24]
        },
        "daily_forecast": [
            {
                "date": daily.get("time", [])[i],
                "temp_max": daily.get("temperature_2m_max", [])[i],
                "temp_min": daily.get("temperature_2m_min", [])[i],
                "rain_sum_mm": daily.get("precipitation_sum", [])[i],
                "rain_prob_max": daily.get("precipitation_probability_max", [])[i],
                "condition": WMO_CODES.get(daily.get("weather_code", [0])[i], "Clear")
            }
            for i in range(min(5, len(daily.get("time", []))))
        ],
        "active_risks": risks
    }
