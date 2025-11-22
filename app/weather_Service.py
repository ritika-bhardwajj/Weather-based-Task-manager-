'''import requests
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
'''

import requests
import logging
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

        # If cache is present and fresh, use it
        if cached and now - cached["timestamp"] < self.cache_duration:
            return cached["data"]

        # BUILDING API URL
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"q={location}&appid={self.api_key}&units=metric"
        )
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            self.cache[location] = {"data": data, "timestamp": now}
            return data
        except Exception as e:
            # If API call fails, fallback to any previous cache (even if stale)
            if cached:
                logging.warning(f"Weather API failed for {location}, using stale cache. Reason: {e}")
                return cached["data"]
            else:
                logging.error(f"Weather API failed for {location}, no cache available. Reason: {e}")
                # Return a safe default dict
                return {
                    "weather": [{"main": ""}],
                    "wind": {"speed": 0}
                }
