from . import models
from .database import db
from .exceptions import NotFoundError, NotUniqueError, AlreadyInDatabaseError


class Manager:

    def __init__(self):
        self.db = db
        self.create_table()

    @property
    def last_id(self):
        rows = self.db.query("""
            SELECT LAST_INSERT_ID() AS id
        """)

        for row in rows:
            return row['id']


class StoreManager(Manager):

    def create_table(self):
        self.db.query("""
            CREATE TABLE IF NOT EXISTS store (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) UNIQUE NOT NULL
            )
        """)

    def add_products(self, store, products):
        for product in products:
            self.add_product(store, product)

    def add_product(self, store, product):
        self.db.query("""
            INSERT IGNORE INTO product_store(product_id, store_id)
            VALUES (:product_id, :store_id)
        """, product_id=product.id, store_id=store.id)

    def get_products(self, store):
        products = self.db.query(f"""
            SELECT product.id, product.name from store
            JOIN product_store ON product_store.store_id = store.id
            JOIN product ON product_store.product_id = product.id
            WHERE store.id = :id
        """, id=store.id).all(as_dict=True)
        return [models.Product(**product) for product in products]

    def save(self, store):
        self.db.query("""
            INSERT INTO store (id, name)
            VALUES (:id, :name)
            ON DUPLICATE KEY UPDATE  name = :name
        """, **vars(store))

        stores = self.get(**vars(store))
        store.id = stores[0].id
        return store

    def create(self, name, id=None, **kwargs):
        return self.save(models.Store(id=id, name=name))

    def get(self, **search_terms):
        conditions = " AND ".join(
            f"{term} = :{term}" 
            for term, value in search_terms.items() 
            if value is not None
        )

        stores = self.db.query(f"""
            SELECT * from store WHERE {conditions}
        """, **search_terms).all(as_dict=True)
        stores = [models.Store(**store) for store in stores]

        if not stores:
            raise NotFoundError(
                "No store was found with the given search terms."
            )
        elif len(stores) > 1:
            raise NotUniqueError(
                "More than one store was found with the given search terms."
            )
            
        return stores[0]

    def get_or_create(self, **search_terms):
        try:
            return self.get(**search_terms)
        except NotFoundError:
            return self.create(**search_terms)

    def get_by_product(self, product):
        stores = self.db.query(f"""
            SELECT * from store
            JOIN product_store ON product_store.store_id = store.id
            JOIN product ON product_store.product_id = product_id
            WHERE product.id = :id
        """, id=product.id).all(as_dict=True)
        return [models.Store(**store) for store in stores]

    def all(self):
        stores = self.db.query(f"""
            SELECT * from store
        """).all(as_dict=True)
        return [models.Store(**store) for store in stores]

    def filter(self, order_by=None, **search_terms):
        conditions = " AND ".join(
            f"{term} = :{term}" 
            for term, value in search_terms.items() 
            if value is not None
        )
        order = ", ".join(order_by) if order_by else 1

        stores = self.db.query(f"""
            SELECT * from store 
            WHERE {conditions}
            ORDER_BY {order}
        """, **search_terms).all(as_dict=True)
        return [models.Store(**store) for store in stores]


class ProductManager(Manager):

    def create_table(self):
        self.db.query("""
            CREATE TABLE IF NOT EXISTS product (
                id BIGINT PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            )
        """)

        self.db.query("""
            CREATE TABLE IF NOT EXISTS product_store (
                product_id BIGINT REFERENCES product(id),
                store_id INT REFERENCES product(id),
                PRIMARY KEY(product_id, store_id)
            )
        """)

    def add_stores(self, product, stores):
        for store in stores:
            self.add_store(product, store)

    def add_store(self, product, store):
        self.db.query("""
            INSERT IGNORE INTO product_store(product_id, store_id)
            VALUES (:product_id, :store_id)
        """, product_id=product.id, store_id=store.id)

    def get_stores(self, product):
        stores = self.db.query(f"""
            SELECT store.id, store.name from store
            JOIN product_store ON product_store.store_id = store.id
            JOIN product ON product_store.product_id = product.id
            WHERE product.id = :id
        """, id=product.id).all(as_dict=True)
        return [models.Store(**store) for store in stores]

    def save(self, product):
        self.db.query("""
            INSERT INTO product (id, name)
            VALUES (:id, :name)
            ON DUPLICATE KEY UPDATE  name = :name
        """, **vars(product))

        if product.id is None:
            product.id = self.last_id
        return product

    def create(self, name, id=None, **kwargs):
        return self.save(models.Product(id=id, name=name))

    def create_from_openfoodfacts(self, code, product_name, stores, **kwargs):
        if not stores.strip():
            raise TypeError("stores must be a non-blank field")

        product = self.get_or_create(
            id=code, 
            name=product_name.lower().strip()
        )
        for store in stores.split(','):
            store = models.Store.objects.get_or_create(
                name=store.lower().strip()
            )
            self.add_store(product, store)
        return product

    def get(self, **search_terms):
        conditions = " AND ".join(
            f"{term} = :{term}" 
            for term, value in search_terms.items() 
            if value is not None
        )

        products = self.db.query(f"""
            SELECT * from product WHERE {conditions}
        """, **search_terms).all(as_dict=True)
        products = [models.Product(**product) for product in products]

        if not products:
            raise NotFoundError(
                "No product was found with the given search terms."
            )
        elif len(products) > 1:
            raise NotUniqueError(
                "More than one product was found with the given search terms."
            )
            
        return products[0]

    def get_or_create(self, **search_terms):
        try:
            return self.get(**search_terms)
        except NotFoundError:
            return self.create(**search_terms)

    def get_by_store(self, store):
        products = self.db.query(f"""
            SELECT * from store
            JOIN product_store ON product_store.store_id = store.id
            JOIN product ON product_store.product_id = product_id
            WHERE store.id = :id
        """, id=store.id).all(as_dict=True)
        return [models.Product(**product) for product in products]

    def all(self):
        products = self.db.query(f"""
            SELECT * from product
        """).all(as_dict=True)
        return [models.Product(**product) for product in products]

    def filter(self, order_by=None, **search_terms):
        conditions = " AND ".join(
            f"{term} = :{term}" 
            for term, value in search_terms.items() 
            if value is not None
        )
        order = ", ".join(order_by) if order_by else 1

        products = self.db.query(f"""
            SELECT * from product
            WHERE {conditions}
            ORDER_BY {order}
        """, **search_terms).all(as_dict=True)
        return [models.Product(**product) for product in products]