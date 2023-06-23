# Third Party Library
import pytest
import pytest_asyncio
import starlette.status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# First Party Library
from api.db import Base, get_db
from api.main import app

ASYNC_DB_URL = "sqlite+aiosqlite:///:memory"


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    """Test Fixture テスト用DBの初期化とテスト用DBセッションの作成
    Return: AsyncClient
    """

    async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
    async_session = sessionmaker(
        autoflush=False, bind=async_engine, class_=AsyncSession
    )

    # SQLiteテーブルの初期化
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async def get_test_db():
        """テスト用DBセッション.こいつをオーバーライドさせることでプロダクションコードに影響を与えない."""

        async with async_session() as session:
            yield session

    app.dependency_overrides[get_db] = get_test_db

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_create_and_read(async_client):
    response = await async_client.post("/tasks", json={"title": "Test Task"})
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["title"] == "Test Task"

    response = await async_client.get("/tasks")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["title"] == "Test Task"
    assert response_obj[0]["done"] is False


@pytest.mark.asyncio
async def test_due_date(async_client):
    response = await async_client.post(
        "/tasks", json={"title": "Test Task", "due_date": "2024-12-40"}
    )

    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_done_flag(async_client):
    response = await async_client.post("/tasks", json={"title": "Test Task2"})
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["title"] == "Test Task2"

    response = await async_client.put("/tasks/1/done")
    assert response.status_code == starlette.status.HTTP_200_OK

    response = await async_client.put("/tasks/1/done")
    assert response.status_code == starlette.status.HTTP_400_BAD_REQUEST

    response = await async_client.delete("/tasks/1/done")
    assert response.status_code == starlette.status.HTTP_200_OK

    response = await async_client.delete("/tasks/1/done")
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND
