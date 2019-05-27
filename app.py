from pprint import pprint

import requests

from demo.models import Product, Store

class ProductDownloader:

    def fetch(self, category, number=20):
        payload = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": category,
            "page_size": number,
            "json": 1,
        }

        response = requests.get("https://fr.openfoodfacts.org/cgi/search.pl", params=payload)
        data = response.json()
        return data['products']


def main():
    downloader = ProductDownloader()
    products = downloader.fetch('pizza', 500)
    
    for product in products:
        try:
            product = Product.objects.create_from_openfoodfacts(**product)
        except TypeError:
            continue

    store = Store.objects.get(id=2)
    print(store)
    for product in store.products:
        print(product)


if __name__ == "__main__":
    main()