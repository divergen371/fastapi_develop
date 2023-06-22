# Third Party Library
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import api.schemas.task as task_schema
import api.cruds.tasks as task_crud
from api.db import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get(path="", response_model=list[task_schema.Task])
async def list_tasks(db: Session = Depends(get_db)):
    return task_crud.get_tasks_with_done(db=db)


@router.post(path="", response_model=task_schema.TaskCreateResponse)
async def create_task(
    task_body: task_schema.TaskCreate, db: Session = Depends(get_db)
):
    return task_crud.create_task(db=db, task_create=task_body)


@router.put(path="/{task_id}", response_model=task_schema.TaskCreateResponse)
async def update_task(
    task_id: int,
    task_body: task_schema.TaskCreate,
    db: Session = Depends(get_db),
):
    task = task_crud.get_task(db=db, task_id=task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found."
        )
    return task_crud.update_task(db=db, task_create=task_body, original=task)


@router.delete(path="/{task_id}", response_model=None)
async def task_delete(task_id: int, db: Session = Depends(get_db)):
    task = task_crud.get_task(db=db, task_id=task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task_crud.delete_task(db, original=task)
