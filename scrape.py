#!/usr/bin/env python3

import api
import storage
from pprint import pprint
import logging


def sync_sales():
    page = 1
    found = 0
    next_page = page + 1

    while True:
        html = api.fetch_page(page)
        (sales, next_page) = api.parse_page(html)

        logging.info(f"parsed page {page}, next page {next_page}")

        found += len(sales)

        storage.save_to_db("asuntojen_hinnat.db3", sales)

        if next_page <= page:
            break

        page = next_page

    logging.info(f"fetched {found} sales")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    sync_sales()
