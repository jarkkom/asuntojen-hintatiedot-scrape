CREATE TABLE IF NOT EXISTS
asuntojen_hinnat (
    id TEXT PRIMARY KEY,
    district TEXT,
    description TEXT,
    building_type TEXT,
    m2 NUMERIC,
    price INTEGER,
    price_per_m2 NUMERIC,
    year INTEGER,
    floor TEXT,
    elevator TEXT,
    condition TEXT,
    lot TEXT,
    energy_class TEXT
)
