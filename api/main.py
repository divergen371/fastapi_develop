# Third Party Library
from fastapi import FastAPI

# First Party Library
from .routers import done, task

app = FastAPI()


app.include_router(router=task.router)
app.include_router(router=done.router)
