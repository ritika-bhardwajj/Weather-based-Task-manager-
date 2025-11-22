import os
import logging
from flask import Flask, jsonify, request
from app.models import Task, TaskCategory, TaskState
from app.store import TaskStore
from app.weather_Service import WeatherService
from app.business_logic import calculate_weather_impact
from app.external_api import get_location, is_holiday
from datetime import datetime

logging.basicConfig(level=logging.INFO)   

app = Flask(__name__)
store = TaskStore()
weather_service = WeatherService(api_key=os.getenv("OPENWEATHER_API_KEY"))
logger = logging.getLogger(__name__)

logger.info("Weather Task Manager started") 

def as_task_dict(t):
    return {
        "id": t.id,
        "title": t.title,
        "description": t.description,
        "category": t.category.value,
        "scheduled_date": t.scheduled_date.isoformat(),
        "location": t.location,
        "state": t.state.value,
        "priority": t.priority,
    }


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/state-machine")
def state_machine():
    """Returns all valid task states."""
    return jsonify({s.name: s.value for s in TaskState}), 200

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    try:
        # === Strict Input Validation Section ===
        required_fields = ["id", "title", "description", "category", "scheduledDate", "priority"]
        missing_fields = [f for f in required_fields if f not in data]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        # Check category validity
        try:
            category = TaskCategory(data["category"])
        except Exception:
            return jsonify({"error": "Invalid category. Use one of: outdoor, indoor, delivery, travel"}), 400

        # Validate scheduledDate format
        try:
            scheduled_date = datetime.fromisoformat(data["scheduledDate"])
        except Exception:
            return jsonify({"error": "scheduledDate must be in ISO format (YYYY-MM-DDTHH:MM:SS)"}), 400

        # Validate priority is an integer
        if not isinstance(data["priority"], int):
            return jsonify({"error": "priority must be an integer"}), 400

        location = data.get("location")
        if not location:
            loc_info = get_location()
            location = loc_info['city']

        # === Proceed to creating the Task as before ===
        task = Task(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            category=category,
            scheduled_date=scheduled_date,
            location=location,
            state=TaskState.SCHEDULED,
            priority=data["priority"]
        )
        store.add(task)
        return jsonify({"message": "Task created"}), 201

    except Exception as e:
        logger.error(str(e))
        return jsonify({"error": "Invalid input"}), 400

'''
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    try:
        location = data.get("location")
        if not location:
            loc_info = get_location()
            location = loc_info['city']
        task = Task(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            category=TaskCategory(data["category"]),
            scheduled_date=datetime.fromisoformat(data["scheduledDate"]),
            location=location,
            state=TaskState.SCHEDULED,
            priority=data["priority"]
        )
        store.add(task)
        return jsonify({"message": "Task created"}), 201
    except Exception as e:
        logger.error(str(e))
        return jsonify({"error": "Invalid input"}), 400
'''

@app.route("/tasks", methods=["GET"])
def list_tasks():
    tasks = store.get_all()

    # FILTERING 
    category = request.args.get("category")
    location = request.args.get("location")
    state = request.args.get("state")
    if category:
        tasks = [t for t in tasks if t.category.value == category.lower()]
    if location:
        tasks = [t for t in tasks if t.location.lower() == location.lower()]
    if state:
        tasks = [t for t in tasks if t.state.value == state.lower()]

    # SORTING
    sort_by = request.args.get("sort_by")
    sort_order = request.args.get("sort_order", "asc")
    if sort_by:
        reverse = (sort_order == "desc")
        if sort_by == "scheduled_date":
            tasks = sorted(tasks, key=lambda t: t.scheduled_date, reverse=reverse)
        elif sort_by == "priority":
            tasks = sorted(tasks, key=lambda t: t.priority, reverse=reverse)

    result = []
    for t in tasks:
        weather = weather_service.fetch_weather(t.location)
        impact = calculate_weather_impact(t, weather)
        
        # LOGGING AUTO DELAYED TASKS
        if not impact["canProceed"] and t.state == TaskState.SCHEDULED and t.category in [
            TaskCategory.OUTDOOR, TaskCategory.DELIVERY, TaskCategory.TRAVEL]:
            logger.info(f"Task '{t.title}' (ID: {t.id}) weather delayed: {impact.get('reason', 'Unknown')}")
        country_code = get_location()['country_code']
        hol, hname = is_holiday(t.scheduled_date, country_code)
        t_dict = as_task_dict(t)
        t_dict.update({
            "weatherImpact": impact,
            "isHoliday": hol,
            "holidayName": hname
        })
        result.append(t_dict)
    return jsonify(result), 200


@app.route("/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    t = store.get(task_id)
    if not t:
        return jsonify({"error": "Task not found"}), 404
    weather = weather_service.fetch_weather(t.location)
    impact = calculate_weather_impact(t, weather)

    # LOGGING FOR VISIBILITY ISSUE
    if not impact["canProceed"] and t.state == TaskState.SCHEDULED and t.category in [
        TaskCategory.OUTDOOR, TaskCategory.DELIVERY, TaskCategory.TRAVEL]:
        logger.info(f"Task '{t.title}' (ID: {t.id}) weather delayed: {impact.get('reason', 'Unknown')}")
    country_code = get_location()['country_code']
    hol, hname = is_holiday(t.scheduled_date, country_code)
    t_dict = as_task_dict(t)
    t_dict.update({
        "weatherImpact": impact,
        "isHoliday": hol,
        "holidayName": hname
    })
    return jsonify(t_dict), 200


@app.route("/tasks/<task_id>/state", methods=["PUT"])
def update_task_state(task_id):
    t = store.get(task_id)
    if not t:
        return jsonify({"error": "Task not found"}), 404
    state = request.json.get("state")
    try:
        t.state = TaskState(state)
    except Exception as e:
        logger.error(str(e))
        return jsonify({"error": "Invalid state"}), 400
    return jsonify({"message": "State updated"}), 200


@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    store.delete(task_id)
    return jsonify({"message": "Task deleted"}), 200


@app.route("/tasks/<task_id>/weather-impact", methods=["GET"])
def weather_impact(task_id):
    t = store.get(task_id)
    if not t:
        return jsonify({"error": "Task not found"}), 404
    weather = weather_service.fetch_weather(t.location)
    impact = calculate_weather_impact(t, weather)
    return jsonify(impact), 200


@app.route("/tasks/bulk-weather-check", methods=["POST"])
def bulk_weather_check():
    tasks = store.get_all()
    result = []
    for t in tasks:
        if t.state == TaskState.SCHEDULED:
            weather = weather_service.fetch_weather(t.location)
            impact = calculate_weather_impact(t, weather)
            result.append({"id": t.id, "impact": impact})
    return jsonify(result), 200


@app.route("/tasks/<task_id>/holiday-check", methods=['GET'])
def holiday_check(task_id):
    t = store.get(task_id)
    if not t:
        return jsonify({"error": "Task not found"}), 404
    country_code = get_location()['country_code']
    hol, hname = is_holiday(t.scheduled_date, country_code)
    return jsonify({
        "isHoliday": hol,
        "holidayName": hname if hol else None
    })
