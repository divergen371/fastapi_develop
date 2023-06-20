from fastapi import APIRouter

router = APIRouter()


@router.put(path="/tasks/{task_id}/done")
async def mark_task_as_done():
    pass


@router.delete(path="/tasks/{task_id}/done")
async def unmark_task_as_done():
    pass
