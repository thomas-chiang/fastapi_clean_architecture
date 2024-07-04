from ....application.port.outward.task_port import TaskPort
from typing import Dict, List
from ....application.domain.model.task import Task
from ....application.domain.model.status import Status


class TaskRepository(TaskPort):
    def __init__(self, db: Dict):
        self.__db = db

    async def list_tasks(self) -> List[Task]:
        return [
            Task(
                id=id,
                name=task.get("name", ""),
                status=Status(value=task.get("status", 0)),
            )
            for id, task in self.__db.items()
        ]

    async def create_task(self, name: str) -> Task:
        id: int = len(self.__db) + 1
        self.__db[id] = {"name": name, "status": Status.incomplete.value}
        return Task(id=id, name=name, status=Status.incomplete)

    async def update_task(self, name: str, status: Status, id: int) -> Task:
        if id not in self.__db:
            raise TaskRepositoryTaskNotFoundError(task_id=id)

        self.__db[id] = {"name": name, "status": status.value}
        return Task(id=id, name=name, status=status)

    async def delete_task(self, id: int) -> None:
        if id not in self.__db:
            raise TaskRepositoryTaskNotFoundError(task_id=id)

        del self.__db[id]


class TaskRepositoryTaskNotFoundError(Exception):
    def __init__(self, task_id):
        self.task_id = task_id
        self.message = f"Task id: {task_id} not found in TaskRepository"
        super().__init__(self.message)
