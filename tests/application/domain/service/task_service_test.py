import pytest
from typing import List
from src.application.port.outward.task_port import TaskPort
from src.application.domain.model.task import Task
from src.application.domain.model.status import Status
from src.application.domain.service.task_service import (
    TaskService,
    TaskServiceTaskNotFoundError,
)
from src.adapter.outward.persistence.task_repository import (
    TaskRepositoryTaskNotFoundError,
)

class MockTaskPort(TaskPort):
    def __init__(self):
        self.tasks = {
            1: Task(id=1, name="Task 1", status=Status.incomplete),
            2: Task(id=2, name="Task 2", status=Status.complete),
        }

    async def list_tasks(self) -> List[Task]:
        return list(self.tasks.values())

    async def create_task(self, name: str) -> Task:
        new_task_id = max(self.tasks.keys(), default=0) + 1
        new_task = Task(id=new_task_id, name=name, status=Status.incomplete)
        self.tasks[new_task_id] = new_task
        return new_task

    async def update_task(self, name: str, status: Status, id: int) -> Task:
        if id in self.tasks:
            updated_task = Task(id=id, name=name, status=status)
            self.tasks[id] = updated_task
            return updated_task
        else:
            raise TaskRepositoryTaskNotFoundError(task_id=id)

    async def delete_task(self, id: int) -> None:
        if id in self.tasks:
            del self.tasks[id]
        else:
            raise TaskRepositoryTaskNotFoundError(task_id=id)

@pytest.mark.asyncio
class TestTaskService:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.mock_task_port = MockTaskPort()
        self.task_service = TaskService(task_port=self.mock_task_port)

    async def test_list_tasks(self):
        tasks = await self.task_service.list_tasks()
        assert len(tasks) == 2
        assert isinstance(tasks[0], Task)
        assert isinstance(tasks[1], Task)

    async def test_create_task(self):
        new_task_name = "New Task"
        new_task = await self.task_service.create_task(name=new_task_name)
        assert new_task.name == new_task_name
        assert new_task.status == Status.incomplete

    async def test_update_task(self):
        task_id = 1
        new_task_name = "Updated Task"
        new_task_status = Status.complete

        updated_task = await self.task_service.update_task(
            new_task_name, new_task_status, task_id
        )
        assert updated_task.name == new_task_name
        assert updated_task.status == new_task_status

    async def test_update_task_not_found(self):
        task_id = 999  # Non-existent task id in MockTaskPort
        with pytest.raises(TaskServiceTaskNotFoundError):
            await self.task_service.update_task("Updated Task", Status.complete, task_id)

    async def test_delete_task(self):
        task_id = 2
        await self.task_service.delete_task(task_id)
        remaining_tasks = await self.mock_task_port.list_tasks()
        assert len(remaining_tasks) == 1
        assert task_id not in [task.id for task in remaining_tasks]

    async def test_delete_task_not_found(self):
        task_id = 999  # Non-existent task id in MockTaskPort
        with pytest.raises(TaskServiceTaskNotFoundError):
            await self.task_service.delete_task(task_id)
