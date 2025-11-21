from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class TaskState(Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    WEATHER_DELAYED = "weather_delayed"
    RESCHEDULED = "rescheduled"
    COMPLETED = "completed"

class TaskCategory(Enum):
    OUTDOOR = "outdoor"
    DELIVERY = "delivery"
    INDOOR = "indoor"
    TRAVEL = "travel"

@dataclass
class Task:
    id: str
    title: str
    description: str
    category: TaskCategory
    scheduled_date: datetime
    location: str
    state: TaskState
    priority: int
