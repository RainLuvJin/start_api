# 测试：创建 Session 是否成功。
from fastapi.testclient import TestClient

from main import app, sessions

client = TestClient(app)


def test_create_session():
    sessions.clear() # 先清空字典里的全部内容
    # 用客户端发个post请求
    response = client.post(
        "/sessions",
        json={
            "username": "Jinny",
            "info": "Learning FastAPI",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "created"
    assert data["session_id"]
    assert data["session_id"] in sessions

def test_get_session():
    sessions.clear()

    create_response = client.post(
        "/sessions",
        json={
            "username": "Jinny",
            "info": "Learning FastAPI",
        },
    )

    session_id = create_response.json()["session_id"]

    response = client.get(f"/sessions/{session_id}")

    assert response.status_code == 200
    assert response.json()["username"] == "Jinny"
    assert response.json()["info"] == "Learning FastAPI"


def test_get_missing_session():
    sessions.clear()

    response = client.get("/sessions/not-exist")

    assert response.status_code == 404


def test_delete_session():
    sessions.clear()

    create_response = client.post(
        "/sessions",
        json={
            "username": "Jinny",
            "info": "Learning FastAPI",
        },
    )

    session_id = create_response.json()["session_id"]

    delete_response = client.delete(f"/sessions/{session_id}")

    assert delete_response.status_code == 200
    assert delete_response.json()["status"] == "deleted"
    assert session_id not in sessions

    get_response = client.get(f"/sessions/{session_id}")

    assert get_response.status_code == 404