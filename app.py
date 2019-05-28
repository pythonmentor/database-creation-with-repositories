from demo.models import Product, Store
from demo.openfoodfacts import ProductDownloader


def main():
    downloader = ProductDownloader()
    products = downloader.fetch('pizza', 500)

    for product in products:
        try:
            product = Product.create_from_openfoodfacts(**product)
        except TypeError:
            continue

    store = Store.objects.get(name='auchan')
    print(store)
    for product in store.products:
        print(product)


if __name__ == "__main__":
    main()
