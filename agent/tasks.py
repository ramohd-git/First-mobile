"""A tiny JSON-backed task list. The agent's tools are thin wrappers around this."""

import json
from pathlib import Path


class TaskStore:
    def __init__(self, path: Path):
        self.path = path

    def _load(self) -> list[dict]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text())

    def _save(self, tasks: list[dict]) -> None:
        self.path.write_text(json.dumps(tasks, indent=2))

    def list(self) -> list[dict]:
        return self._load()

    def add(self, title: str) -> dict:
        tasks = self._load()
        task = {
            "id": max((t["id"] for t in tasks), default=0) + 1,
            "title": title,
            "done": False,
        }
        tasks.append(task)
        self._save(tasks)
        return task

    def complete(self, task_id: int) -> dict | None:
        tasks = self._load()
        for task in tasks:
            if task["id"] == task_id:
                task["done"] = True
                self._save(tasks)
                return task
        return None

    def delete(self, task_id: int) -> dict | None:
        tasks = self._load()
        for i, task in enumerate(tasks):
            if task["id"] == task_id:
                removed = tasks.pop(i)
                self._save(tasks)
                return removed
        return None
