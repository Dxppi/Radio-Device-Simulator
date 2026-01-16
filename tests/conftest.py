import importlib
import sqlite3

import pytest


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "test.sqlite"
    monkeypatch.setenv("DB_PATH", str(db_path))

    import api.settings as settings
    import repository.radioDevices as repo
    import app as app_module

    importlib.reload(settings)
    importlib.reload(repo)
    importlib.reload(app_module)

    with sqlite3.connect(db_path) as con:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS devices (
                id              INTEGER PRIMARY KEY,
                frequency       REAL,
                power           REAL,
                last_measurement TEXT,
                is_connected    INTEGER
            )
            """
        )

    app_module.application.config["TESTING"] = True
    with app_module.application.test_client() as client:
        yield client


@pytest.fixture
def connected_device(client):
    resp = client.post("/devices", json={"frequency": 2400, "power": 10})
    data = resp.get_json()
    device_id = data["data"]["device_id"]

    resp = client.post(f"/devices/{device_id}/connect")
    assert resp.status_code == 200

    return device_id
