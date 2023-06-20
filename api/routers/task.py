# Third Party Library
from fastapi import APIRouter

import api.schemas.task as task_schema

router = APIRouter(prefix="/tasks")


@router.get(path="", response_model=list[task_schema.Task])
async def list_tasks():
    return [task_schema.Task(id=1, title="1つ目のToDoタスク")]


@router.post(path="", response_model=task_schema.TaskCreateResponse)
async def create_task(task_body: task_schema.TaskCreate):
    return task_schema.TaskCreateResponse(id=1, **task_body.dict())


@router.put(path="/{task_id}", response_model=task_schema.TaskCreateResponse)
async def update_task(task_id: int, task_body: task_schema.TaskCreate):
    return task_schema.TaskCreateResponse(id=task_id, **task_body.dict())


@router.delete(path="/{task_id}", response_model=None)
async def task_delete(task_id: int):
    return
