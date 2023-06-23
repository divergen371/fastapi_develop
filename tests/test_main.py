import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from api.db import get_db, Base
from api.main import app

ASYNC_DB_URL = "sqlite+aiosqlite:///:memory"


@pytest_asyncio.fixture
async def asyncClient():
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
