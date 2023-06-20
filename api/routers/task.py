# Third Party Library
from fastapi import APIRouter

import api.schemas.task as task_schema

router = APIRouter(prefix="/tasks")


@router.get(path="", response_model=list[task_schema.Task])
async def list_tasks():
    return [task_schema.Task(id=1, title="1つ目のToDoタスク")]


@router.post(path="")
async def create_task():
    pass


@router.put(path="{task_id}")
async def update_task():
    pass


@router.delete(path="{task_id}")
async def task_delete():
    pass
