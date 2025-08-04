import sqlite3
from datetime import datetime
from typing import List, Tuple

DB_PATH = "vehicle_data.sqlite"

def insert_vehicle(data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    INSERT OR REPLACE INTO vehicles (
        vin, make, model, year, co2, electricity_efficiency, fuel_type, fetched_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["vin"],
        data.get("make"),
        data.get("model"),
        data.get("year"),
        data.get("co2"),
        data.get("electricity_efficiency"),
        data.get("fuel_type"),
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()

def get_vehicles_by_make_model_year(make: str, model: str, year: int) -> List[Tuple]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT * FROM vehicles
        WHERE LOWER(make) = LOWER(?) AND LOWER(model) = LOWER(?) AND year = ?
    """, (make, model, year))
    rows = c.fetchall()
    conn.close()
    return rows
