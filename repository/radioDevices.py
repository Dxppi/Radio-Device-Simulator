import sqlite3
from datetime import datetime

from api.settings import DB_PATH
from models.radioDevice import RadioDevice


def device_from_row(row) -> RadioDevice:
    device_id, frequency, power, last_meas, is_conn = row
    last_dt = datetime.fromisoformat(last_meas) if last_meas else None
    return RadioDevice(
        device_id=device_id,
        frequency=frequency,
        power=power,
        last_measurement=last_dt,
        is_connected=bool(is_conn),
    )


def get_device(device_id: int) -> RadioDevice | None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
        "SELECT id, frequency, power, last_measurement, is_connected "
        "FROM devices WHERE id = ?",
        (device_id,),
    )
    row = cur.fetchone()
    con.close()
    if row is None:
        return None
    return device_from_row(row)


def insert_device(frequency: int, power: int) -> int:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO devices (frequency, power, last_measurement, is_connected) "
        "VALUES (?, ?, ?, ?)",
        (frequency, power, None, 1),
    )
    con.commit()
    device_id = cur.lastrowid
    con.close()
    return device_id


def save_device(device: RadioDevice) -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    last_meas = device.last_measurement.isoformat() if device.last_measurement else None
    cur.execute(
        """
        UPDATE devices
        SET frequency = ?, power = ?, last_measurement = ?, is_connected = ?
        WHERE id = ?
        """,
        (
            device.frequency,
            device.power,
            last_meas,
            int(device.is_connected),
            device.id,
        ),
    )
    con.commit()
    con.close()
