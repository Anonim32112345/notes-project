from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import get_db, Base

# Настраиваем отдельную тестовую БД (в памяти)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_create_note():
    response = client.post(
        "/api/notes/",
        json={"title": "Тестовая заметка", "content": "Это текст проверки"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Тестовая заметка"

def test_get_notes():
    response = client.get("/api/notes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)