import duckdb
import polars as pl
import os

def create_database(csv_path=None, db_path=None):
    if csv_path is None:
        csv_path = os.path.join(os.path.dirname(__file__), '../data/raw/electric_vehicles_spec_2025.csv')
    if db_path is None:
        db_path = os.path.join(os.path.dirname(__file__), 'ev_vehicles.duckdb')

    df = pl.read_csv(csv_path)
    con = duckdb.connect(db_path)

    con.execute("DROP TABLE IF EXISTS brand;")
    con.execute("DROP TABLE IF EXISTS model;")
    con.execute("DROP TABLE IF EXISTS spec;")

    con.execute("""
    CREATE TABLE brand (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    );
    """)
    con.execute("""
    CREATE TABLE model (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        brand_id INTEGER REFERENCES brand(id)
    );
    """)
    con.execute("""
    CREATE TABLE spec (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_id INTEGER REFERENCES model(id),
        top_speed_kmh INTEGER,
        battery_capacity_kWh DOUBLE,
        battery_type TEXT,
        number_of_cells INTEGER,
        torque_nm INTEGER,
        efficiency_wh_per_km DOUBLE,
        range_km INTEGER,
        acceleration_0_100_s DOUBLE,
        fast_charging_power_kw_dc DOUBLE,
        fast_charge_port TEXT,
        towing_capacity_kg INTEGER,
        cargo_volume_l INTEGER,
        seats INTEGER,
        drivetrain TEXT,
        segment TEXT,
        length_mm INTEGER,
        width_mm INTEGER,
        height_mm INTEGER,
        car_body_type TEXT,
        source_url TEXT
    );
    """)

    brands = df['brand'].unique().to_list()
    for brand in brands:
        con.execute("INSERT INTO brand (name) VALUES (?) ON CONFLICT(name) DO NOTHING;", [brand])

    for row in df.iter_rows(named=True):
        brand_id = con.execute("SELECT id FROM brand WHERE name = ?;", [row['brand']]).fetchone()[0]
        con.execute("INSERT INTO model (name, brand_id) VALUES (?, ?) ON CONFLICT(name, brand_id) DO NOTHING;", [row['model'], brand_id])
        model_id = con.execute("SELECT id FROM model WHERE name = ? AND brand_id = ?;", [row['model'], brand_id]).fetchone()[0]
        con.execute("""
            INSERT INTO spec (
                model_id, top_speed_kmh, battery_capacity_kWh, battery_type, number_of_cells, torque_nm,
                efficiency_wh_per_km, range_km, acceleration_0_100_s, fast_charging_power_kw_dc, fast_charge_port,
                towing_capacity_kg, cargo_volume_l, seats, drivetrain, segment, length_mm, width_mm, height_mm,
                car_body_type, source_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            model_id,
            row['top_speed_kmh'],
            row['battery_capacity_kWh'],
            row['battery_type'],
            row['number_of_cells'],
            row['torque_nm'],
            row['efficiency_wh_per_km'],
            row['range_km'],
            row['acceleration_0_100_s'],
            row['fast_charging_power_kw_dc'],
            row['fast_charge_port'],
            row['towing_capacity_kg'],
            row['cargo_volume_l'],
            row['seats'],
            row['drivetrain'],
            row['segment'],
            row['length_mm'],
            row['width_mm'],
            row['height_mm'],
            row['car_body_type'],
            row['source_url']
        ])
    con.close()
    print(f"Database created at {db_path} with tables: brand, model, spec.")
