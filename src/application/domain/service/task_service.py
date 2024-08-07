from ...port.outward.task_port import TaskPort
from ...port.inward.task_use_case import TaskUseCase
from typing import List
from ..model.task import Task
from ..model.status import Status
from ....adapter.outward.persistence.task_repository import (
    TaskRepositoryTaskNotFoundError,
)


class TaskService(TaskUseCase):
    def __init__(self, task_port: TaskPort):
        self.task_port: TaskPort = task_port

    async def list_tasks(self) -> List[Task]:
        return await self.task_port.list_tasks()

    async def create_task(self, name: str) -> Task:
        return await self.task_port.create_task(name=name)

    async def update_task(self, name: str, status: Status, id: int) -> Task:
        try:
            return await self.task_port.update_task(name=name, status=status, id=id)
        except TaskRepositoryTaskNotFoundError:
            raise TaskServiceTaskNotFoundError(task_id=id)

    async def delete_task(self, id: int) -> None:
        try:
            await self.task_port.delete_task(id)
        except TaskRepositoryTaskNotFoundError:
            raise TaskServiceTaskNotFoundError(task_id=id)


class TaskServiceTaskNotFoundError(Exception):
    def __init__(self, task_id):
        self.task_id = task_id
        self.message = f"Task id: {task_id} not found in TaskService"
        super().__init__(self.message)
