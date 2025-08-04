"""Initialize the SQLite database for vehicle data."""
import sqlite3

def init_db():
    """
    Initializes the SQLite database for vehicle data.
    Creates a connection to 'db/vehicle_data.db' and ensures that the 'vehicles' table exists.
    The 'vehicles' table includes the following columns:
        - vin (TEXT, primary key): Vehicle Identification Number
        - make (TEXT): Manufacturer of the vehicle
        - model (TEXT): Model of the vehicle
        - year (INTEGER): Year of manufacture
        - co2 (REAL): CO2 emissions value
        - electricity_efficiency (REAL): Electricity efficiency value
        - fuel_type (TEXT): Type of fuel used
        - fetched_at (TEXT): Timestamp when the data was fetched
    If the table already exists, no changes are made.
    """
    conn = sqlite3.connect("vehicle_data.sqlite")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS vehicles (
        vin TEXT PRIMARY KEY,
        make TEXT,
        model TEXT,
        year INTEGER,
        co2 REAL,
        electricity_efficiency REAL,
        fuel_type TEXT,
        fetched_at TEXT
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
