from . import managers


class Model:

    def save(self):
        self.objects.save(self)

    def __repr__(self):
        attributes = ", ".join(
            f"{key}={value}" 
            for key, value in vars(self).items()
        )
        return f"{type(self).__name__}(id={self.id}, name={self.name})"


class Store(Model):

    def __init__(self, name, id=None, **kwargs):
        self.id = id
        self.name = name

    @property
    def products(self):
        """Loads related products."""
        return Product.objects.get_all_by_store(self)


Store.objects = managers.StoreManager(Store)


class Product(Model):

    def __init__(self, id, name, **kwargs):
        self.id = id
        self.name = name

    @property
    def stores(self):
        """Loads related stores."""
        return Store.objects.get_all_by_product(self)

    @classmethod
    def create_from_openfoodfacts(cls, code, product_name, stores, **kwargs):
        """Creates store from openfoodfacts data."""
        if not stores.strip():
            raise TypeError("stores must be a non-blank field")

        product = cls.objects.get_or_create(
            id=code, 
            name=product_name.lower().strip()
        )
        for store in stores.split(','):
            store = Store.objects.get_or_create(
                name=store.lower().strip()
            )
            cls.objects.add_store(product, store)
        return product


Product.objects = managers.ProductManager(Product)




    
