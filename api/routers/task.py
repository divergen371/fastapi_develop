# Third Party Library
from fastapi import APIRouter

router = APIRouter(prefix="/tasks")


@router.get(path="")
async def list_tasks():
    pass


@router.post(path="")
async def create_task():
    pass


@router.put(path="{task_id}")
async def update_task():
    pass


@router.delete(path="{task_id}")
async def task_delete():
    pass
