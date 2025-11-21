from typing import Dict, List, Optional
from app.models import Task

class TaskStore:

    def __init__(self):
        self.tasks: Dict[str, Task] = {}  # key: task ID, value: Task object

    def get_all(self) -> List[Task]:
        return list(self.tasks.values())

    def get(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)

    def add(self, task: Task):
        self.tasks[task.id] = task

    def update(self, task_id: str, **kwargs):
        task = self.tasks.get(task_id)
        if not task:
            return
        for k, v in kwargs.items():
            if hasattr(task, k):
                setattr(task, k, v)

    def delete(self, task_id: str):
        if task_id in self.tasks:
            del self.tasks[task_id]
