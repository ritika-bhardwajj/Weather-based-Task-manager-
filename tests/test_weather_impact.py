from app.business_logic import calculate_weather_impact
from app.models import Task, TaskCategory, TaskState
from app.store import TaskStore
from datetime import datetime

# UNIT TESTS
def test_outdoor_rain():
    task = Task("1", "Outdoor", "desc", TaskCategory.OUTDOOR, datetime.now(), "London", TaskState.SCHEDULED, 1)
    weather = {"weather": [{"main": "Rain"}], "wind": {"speed": 5}}
    result = calculate_weather_impact(task, weather)
    assert not result["canProceed"]
    assert result["riskLevel"] == "high"

def test_indoor_any():
    task = Task("2", "Indoor Task", "desc", TaskCategory.INDOOR, datetime.now(), "London", TaskState.SCHEDULED, 1)
    weather = {"weather": [{"main": "Rain"}], "wind": {"speed": 25}}
    result = calculate_weather_impact(task, weather)
    assert result["canProceed"]
    assert result["riskLevel"] == "low"

def test_store_add_and_get():
    store = TaskStore()
    task = Task("3", "Test Store", "desc", TaskCategory.OUTDOOR, datetime.now(), "London", TaskState.SCHEDULED, 2)
    store.add(task)
    assert store.get("3") == task

def test_store_delete():
    store = TaskStore()
    task = Task("4", "Test Remove", "desc", TaskCategory.DELIVERY, datetime.now(), "London", TaskState.SCHEDULED, 2)
    store.add(task)
    store.delete("4")
    assert store.get("4") is None

def test_category_value():
    task = Task("5", "EnumTest", "desc", TaskCategory.TRAVEL, datetime.now(), "London", TaskState.SCHEDULED, 3)
    assert task.category.value == "travel"

# STATE MACHINE INTEGRATION TEST
import pytest
from app.main import app

def test_state_machine_endpoint():
    with app.test_client() as client:
        resp = client.get("/state-machine")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "SCHEDULED" in data
        assert data["SCHEDULED"] == "scheduled"
