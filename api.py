import requests
from bs4 import BeautifulSoup
import hashlib
import logging


def get_id(s):
    h = hashlib.md5()
    h.update(bytes(s, "utf-8"))
    return h.hexdigest()


def fetch_page(z):
    params = {
        "c": "Helsinki",  # Kaupunki
        "cr": "1",  # Postinumero vai Kaupunginosa
        "h": "1",  # Talotyyppi
        "r": 4,  # Huoneet
        #        "t": 3, # ?
        #        "l": 0, # ?
        #        "z": str(z), # Sivunumero
        #    "nc": "167", # Kaupunginosakoodi
        "amin": "100.0",  # Asuinpinta-ala
        "amax": "",  # Asuinpinta-ala
        "sf": 0,  # Sortt field?
        "so": "a",  # Sort order a = ascending, d = descending
        "search": 1,
        "renderType": "renderTypeTable",  # Taulukko/kartta
        "print": "0",
    }
    if z > 0:
        params["z"] = z

    api_resp = requests.get("https://asuntojen.hintatiedot.fi/haku/", params=params)

    if api_resp.status_code == 200:
        logging.info(f"fetch page {z} succesfully")
        return api_resp.text

    logging.error(f"error fetching sales: {api_resp.status_code}")

    return None


def convert_sale(sale):
    sale["m2"] = float(str.replace(sale["m2"], ",", "."))
    sale["price"] = float(str.replace(sale["price"], ",", "."))
    sale["price_per_m2"] = float(str.replace(sale["price_per_m2"], ",", "."))
    sale["year"] = int(sale["year"])

    return sale


def parse_page(html):
    soup = BeautifulSoup(html, "html5lib")

    sales = []

    i = 0
    for first_td in soup.find_all("td", class_="neighborhood"):
        sale = {}
        sale["district"] = first_td.string
        keys = [
            "description",
            "building_type",
            "m2",
            "price",
            "price_per_m2",
            "year",
            "floor",
            "elevator",
            "condition",
            "lot",
            "energy_class",
        ]
        for td in first_td.find_next_siblings("td"):
            key = keys.pop(0)
            sale[key] = "".join(td.stripped_strings)

        raw_id = "|".join(sale.values())
        hashed_id = get_id(raw_id)
        sale["id"] = hashed_id

        sale = convert_sale(sale)

        sales.append(sale)

        i += 1

    next_z = 0

    for navigation in soup.find_all("input", attrs={"type": "hidden", "name": "z"}):
        nav_z = int(navigation["value"])
        next_z = max(next_z, nav_z)

    return sales, next_z
