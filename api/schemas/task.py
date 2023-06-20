from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: str | None = Field(default=None, example="クリーニングを取りに行く")


class TaskCreate(TaskBase):
    pass


class TaskCreateResponse(TaskCreate):
    task_create_id: int

    class Config:
        orm_mode = True


class Task(TaskBase):
    task_id: int
    done: bool = Field(False, description="完了フラグ")

    class Config:
        orm_mode = True
