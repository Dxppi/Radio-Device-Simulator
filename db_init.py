import sqlite3
from api.settings import DB_PATH

con = sqlite3.connect(DB_PATH)
cur = con.cursor()

cur.execute(
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

con.commit()
con.close()
