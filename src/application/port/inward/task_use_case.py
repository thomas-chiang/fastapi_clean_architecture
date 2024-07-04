from abc import ABC, abstractmethod
from typing import List
from ...domain.model.task import Task
from ...domain.model.status import Status


class TaskUseCase(ABC):
    @abstractmethod
    async def list_tasks(self) -> List[Task]:
        pass

    @abstractmethod
    async def create_task(self, name: str) -> Task:
        pass

    @abstractmethod
    async def update_task(self, name: str, status: Status, id: int) -> Task:
        pass

    @abstractmethod
    async def delete_task(self, id: int) -> None:
        pass
