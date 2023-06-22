# Third Party Library
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import api.schemas.task as task_schema
import api.cruds.tasks as task_crud
from api.db import get_db

router = APIRouter(prefix="/tasks")


@router.get(path="", response_model=list[task_schema.Task])
async def list_tasks(db: Session = Depends(get_db)):
    return task_crud.get_tasks_with_done(db)


@router.post(path="", response_model=task_schema.TaskCreateResponse)
async def create_task(
    task_body: task_schema.TaskCreate, db: Session = Depends(get_db)
):
    return task_crud.create_task(db, task_body)


@router.put(path="/{task_id}", response_model=task_schema.TaskCreateResponse)
async def update_task(task_id: int, task_body: task_schema.TaskCreate):
    return task_schema.TaskCreateResponse(id=task_id, **task_body.dict())


@router.delete(path="/{task_id}", response_model=None)
async def task_delete(task_id: int):
    return
