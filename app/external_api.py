import requests
from datetime import datetime

def get_location(ip=''):
    url = f"https://ipapi.co/{ip}/json/" if ip else "https://ipapi.co/json/"
    resp = requests.get(url, timeout=10)
    data = resp.json()
    return {
        'city': data.get('city'),
        'region': data.get('region'),
        'country': data.get('country_name'),
        'country_code': data.get('country_code')
    }

def is_holiday(date: datetime, country_code: str):
    year = date.year
    date_str = date.strftime("%Y-%m-%d")
    url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/{country_code}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200 or not resp.text.strip():
            return False, ""
        holidays = resp.json()
        if not isinstance(holidays, list):
            return False, ""
        for h in holidays:
            if isinstance(h, dict) and h.get('date') == date_str:
                return True, h.get('localName', "")
        return False, ""
    except Exception as e:
        return False, ""

