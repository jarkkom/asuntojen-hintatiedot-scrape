import requests
import logging
from pprint import pprint
from bs4 import BeautifulSoup
import hashlib
import storage

def get_id(s):
    h = hashlib.md5()
    h.update(bytes(s, 'utf-8'))
    return h.hexdigest()

def fetch_page(z):
    params = {
        "c": "Helsinki", # Kaupunki
        "cr": "1", # Postinumero vai Kaupunginosa
        "h": "1", # Talotyyppi
        "r": 4, # Huoneet
#        "t": 3, # ?
#        "l": 0, # ?
#        "z": str(z), # Sivunumero
    #    "nc": "167", # Kaupunginosakoodi
        "amin": "100.0", # Asuinpinta-ala
        "amax": "", # Asuinpinta-ala
        "sf": 0, # Sortt field?
        "so": "a", # Sort order a = ascending, d = descending
        "search": 1,
        "renderType": "renderTypeTable", # Taulukko/kartta
        "print": "0",
    }
    if z > 0:
        params['z'] = z

    api_resp = requests.get("https://asuntojen.hintatiedot.fi/haku/", params=params)

    soup = BeautifulSoup(api_resp.text, "html5lib")

    sales = []

    i = 0
    for first_td in soup.find_all("td", class_="neighborhood"):
        sale = {}
        print()
        pprint(first_td.string)
        sale['district'] = first_td.string
        keys = ['description', 'building_type', 'm2', 'price', 'price_per_m2', 'year', 'floor', 'elevator', 'condition', 'lot', 'energy_class']
        for td in first_td.find_next_siblings("td"):
            pprint("".join(td.stripped_strings))
            key = keys.pop(0)
            sale[key] = "".join(td.stripped_strings)

        raw_id = "|".join(sale.values())
        print(raw_id, get_id(raw_id))
        sale['id'] = get_id(raw_id)

        sales.append(sale)

        i += 1

        

    #pprint(i)

    next_z = None

    for navigation in soup.find_all("input", attrs={"type": "hidden", "name": "z"}):
        nav_z = int(navigation['value'])
        if nav_z > z:
            next_z = nav_z
            print(f"next z: {nav_z}")

    return sales, next_z

if __name__ == '__main__':
    page = 1
    while page is not None:
        (sales, page) = fetch_page(page)
        pprint(sales)

        storage.save_to_db("asuntojen_hinnat.db3", sales)
