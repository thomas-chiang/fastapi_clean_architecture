import pytest
import asyncio
from typing import Dict
from src.application.domain.model.task import Task
from src.application.domain.model.status import Status
from src.adapter.outward.persistence.task_repository import (
    TaskRepository,
    TaskRepositoryTaskNotFoundError,
)


class TestTaskRepository:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        # Mock database dictionary
        self.db: Dict[int, Dict[str, any]] = {
            1: {"name": "Task 1", "status": Status.incomplete.value},
            2: {"name": "Task 2", "status": Status.complete.value},
        }
        self.repository = TaskRepository(self.db)

    @pytest.mark.asyncio
    async def test_list_tasks(self):
        tasks = await self.repository.list_tasks()
        assert len(tasks) == len(self.db)
        for task in tasks:
            assert isinstance(task, Task)

    @pytest.mark.asyncio
    async def test_create_task(self):
        new_task_name = "New Task"
        new_task = await self.repository.create_task(new_task_name)
        assert new_task.name == new_task_name
        assert new_task.status == Status.incomplete

    @pytest.mark.asyncio
    async def test_update_task(self):
        task_id = 1
        new_task_name = "Updated Task"
        new_task_status = Status.complete

        updated_task = await self.repository.update_task(
            new_task_name, new_task_status, task_id
        )
        assert updated_task.name == new_task_name
        assert updated_task.status == new_task_status

    @pytest.mark.asyncio
    async def test_update_task_not_found(self):
        task_id = 999  # Non-existent task id
        with pytest.raises(TaskRepositoryTaskNotFoundError):
            await self.repository.update_task("Updated Task", Status.complete, task_id)

    @pytest.mark.asyncio
    async def test_delete_task(self):
        task_id = 2
        await self.repository.delete_task(task_id)
        assert task_id not in self.db

    @pytest.mark.asyncio
    async def test_delete_task_not_found(self):
        task_id = 999  # Non-existent task id
        with pytest.raises(TaskRepositoryTaskNotFoundError):
            await self.repository.delete_task(task_id)
