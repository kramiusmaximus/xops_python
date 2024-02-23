import time
from fastapi.testclient import TestClient
import pytest
from main import app
from db import Base
from datetime import datetime

client = TestClient(app)


@pytest.fixture()
def test_db():
    Base.metadata.create_all(Base.metadata.bind)
    yield
    Base.metadata.drop_all(Base.metadata.bind)


def test_post_visited_links(test_db):
    response = client.post(
        "/visited_links",
        json={"urls": ["http://example.com", "https://testsite.com"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_get_visited_domains_noargs_valid(test_db):
    response = client.post(
        "/visited_links",
        json={
            "urls": [
                "http://example.com",
                "https://testsite.com",
            ]
        },
    )
    assert response.status_code == 200
    response = client.get("/visited_domains")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "example.com" in data["domains"]
    assert "testsite.com" in data["domains"]
    assert "invalid.com" not in data["domains"]


def test_get_visited_domains_invalid(test_db):
    response = client.post(
        "/visited_links",
        json={
            "urls": [
                "httpx://testsite.com",
            ]
        },
    )
    assert response.status_code == 422
    response = client.get("/visited_domains")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert len(data["domains"]) == 0


def test_get_visited_domains_args(test_db):
    response = client.post(
        "/visited_links",
        json={"urls": ["https://testsiteA.com"]},
    )
    assert response.status_code == 200

    time_delta = 3
    time.sleep(time_delta)

    response = client.post(
        "/visited_links",
        json={"urls": ["https://testsiteb.com"]},
    )
    assert response.status_code == 200

    curr_time = int(datetime.now().timestamp())
    response = client.get(f"/visited_domains?date_from={curr_time - time_delta + 1}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "testsiteb.com" in data["domains"]
    assert "testsitea.com" not in data["domains"]

    response = client.get(f"/visited_domains")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "testsiteb.com" in data["domains"]
    assert "testsitea.com" in data["domains"]
