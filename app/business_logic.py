from datetime import timedelta
from app.models import Task

def calculate_weather_impact(task: Task, weather_data: dict) -> dict:
    main = weather_data.get("weather", [{}])[0].get("main", "")
    wind_speed = weather_data.get("wind", {}).get("speed", 0)
    category = task.category.value.lower()

    can_proceed, reason, risk_level = True, "", "low"
    suggested_date = None
    wind_mph = wind_speed * 2.23694

    # BUSINESS RULES:

    # Outdoor - rain, snow, high wind
    if category == "outdoor":
        if main.lower() in ["rain", "snow"] or wind_mph > 25:
            can_proceed = False
            reason = f"{main} or high wind expected"
            risk_level = "high"
            suggested_date = (task.scheduled_date + timedelta(days=1)).strftime("%Y-%m-%d")

    # Delivery - severe weather
    elif category == "delivery":
        if main.lower() in ["storm", "heavy snow"]:
            can_proceed = False
            reason = f"{main} expected"
            risk_level = "high"

    # Travel - visibility/severe
    elif category == "travel":
        if main.lower() in ["fog", "storm"]:
            can_proceed = False
            reason = f"{main} expected"
            risk_level = "medium"

    # indoor - unaffected

    return {
        "canProceed": can_proceed,
        "reason": reason if reason else "No major weather impact",
        "suggestedDate": suggested_date,
        "riskLevel": risk_level
    }
