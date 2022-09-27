import logging
import sqlite3

FIND_ID_STMT = "SELECT id FROM asuntojen_hinnat WHERE id = :id"

INSERT_STMT = """
INSERT INTO asuntojen_hinnat (
    id, district, description, building_type, m2, price, price_per_m2, year, floor, elevator, condition, lot, energy_class, added
) VALUES (
    :id, :district, :description, :building_type, :m2, :price, :price_per_m2, :year, :floor, :elevator, :condition, :lot, :energy_class, datetime('now')
)"""


def save_to_db(dbfile, sales):
    con = sqlite3.connect(dbfile)
    cur = con.cursor()

    for sale in sales:
        if sale is None:
            continue

        exists_res = cur.execute(FIND_ID_STMT, sale)
        if exists_res.fetchone() is None:
            logging.info(f"new listing {sale['id']}")
            cur.execute(INSERT_STMT, sale)

    con.commit()
