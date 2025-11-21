from app.store import TaskStore
from app.models import Task, TaskCategory, TaskState
from datetime import datetime, timedelta

store = TaskStore()
tasks = [
    Task("1", "Outdoor Clean", "Clean backyard", TaskCategory.OUTDOOR, datetime.now(), "Delhi", TaskState.SCHEDULED, 1),
    Task("2", "Delivery Books", "Delivery for books", TaskCategory.DELIVERY, datetime.now() + timedelta(days=1), "Mumbai", TaskState.DRAFT, 2),
    Task("3", "Indoor Painting", "Paint living room", TaskCategory.INDOOR, datetime.now() + timedelta(days=2), "Delhi", TaskState.SCHEDULED, 1),
    Task("4", "Travel Trip", "Trip to Jaipur", TaskCategory.TRAVEL, datetime.now() + timedelta(days=3), "Jaipur", TaskState.SCHEDULED, 3),
    Task("5", "Lawn Mowing", "Mow lawn", TaskCategory.OUTDOOR, datetime.now() + timedelta(weeks=1), "Delhi", TaskState.SCHEDULED, 2),
]
for t in tasks:
    store.add(t)
print("Seeded tasks.")
