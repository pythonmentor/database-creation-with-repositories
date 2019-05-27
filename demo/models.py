from . import managers

class Model:

    objects = None

    def save(self):
        type(self).objects.save(self)

    def __repr__(self):
        params = ", ".join(
            f"{key}={value}" for key, value in vars(self).items()
        )
        return f"{type(self).__name__}({params})"


class Store(Model):

    objects = managers.StoreManager()

    def __init__(self, name, id=None, **kwargs):
        self.id = id
        self.name = name

    @property
    def products(self):
        """Loads related products."""
        return type(self).objects.get_products(self)
    

class Product(Model):

    objects = managers.ProductManager()

    def __init__(self, id, name, **kwargs):
        self.id = id
        self.name = name

    @property
    def stores(self):
        """Loads related stores."""
        return type(self).objects.get_stores(self)




    
