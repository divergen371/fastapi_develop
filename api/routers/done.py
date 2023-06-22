from fastapi import APIRouter, HTTPException, Depends, status

from sqlalchemy.orm import Session
import api.schemas.done as done_schema
import api.cruds.done as done_crud

from api.db import get_db

router = APIRouter(tags={"done"})


@router.put(
    path="/tasks/{task_id}/done", response_model=done_schema.DoneResponse
)
async def mark_task_as_done(task_id: int, db: Session = Depends(get_db)):
    done = done_crud.get_done(db=db, task_id=task_id)
    if done is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Done already exists.",
        )
    return done_crud.create_done(db=db, task_id=task_id)


@router.delete(path="/tasks/{task_id}/done", response_model=None)
async def unmark_task_as_done(task_id: int, db: Session = Depends(get_db)):
    done = done_crud.get_done(db=db, task_id=task_id)
    if done is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Done not found."
        )
    return done_crud.delete_done(db=db, original=done)
