import requests
from datetime import datetime, timedelta, timezone
from typing import Dict, Any

class WeatherService:

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.cache_duration = timedelta(minutes=10)

    def fetch_weather(self, location: str) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        cached = self.cache.get(location)
        if cached and now - cached["timestamp"] < self.cache_duration:
            return cached["data"]

        # BUILDING API URL
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"q={location}&appid={self.api_key}&units=metric"
        )
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()           
        data = resp.json()
        self.cache[location] = {"data": data, "timestamp": now}
        return data
