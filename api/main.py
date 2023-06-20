from fastapi import FastAPI

app = FastAPI()


@app.get(path="/hello")
async def hello():
    return {"message": "hello world"}
