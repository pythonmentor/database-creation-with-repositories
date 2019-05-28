from .database import db
from .exceptions import NotFoundError, NotUniqueError


class Repository:

    def __init__(self, model):
        """Initializes the repository."""
        self.db = db
        self.model = model
        self.create_table()

    @property
    def last_id(self):
        """Returns the last auto-incremented id."""
        rows = self.db.query("""
            SELECT LAST_INSERT_ID() AS id
        """)

        for row in rows:
            return row['id']

    def filter(self, **search_terms):
        """Searches objects in the database matching the provided criteria."""
        conditions = " AND ".join(
            f"{term} = :{term}"
            for term, value in search_terms.items()
            if value is not None
        ).strip()

        if conditions:
            conditions = f"WHERE {conditions}"

        instances = self.db.query(f"""
            SELECT * from {self.table}
            {conditions}
        """, **search_terms).all(as_dict=True)

        return [
            self.model(**instance)
            for instance in instances
        ]

    def get(self, **search_terms):
        """Gets one object from the database matching the provided criteria."""
        instances = self.filter(**search_terms)

        if not instances:
            raise NotFoundError("Nothing has been found.")

        if len(instances) > 1:
            raise NotUniqueError("Serveral instance have been found.")

        return instances[0]

    def get_or_create(self, **search_terms):
        """Gets one object from the database matching the provided criteria or
        creates it if it does not exist.
        """
        try:
            instance = self.get(**search_terms)
        except NotFoundError:
            instance = self.create(**search_terms)
        return instance

    def all(self):
        """Returns all the objects of the current type in the database."""
        return self.filter()

    def create(self, **attributes):
        """Create a new instance of the model and saves it in the database."""
        return self.save(self.model(**attributes))

    def create_table(self):
        """Creates the necessary tables for the current model to work."""
        pass

    def save(self, instance):
        """Saves or updates the current model instance in the database."""
        return instance


class StoreRepository(Repository):

    table = 'store'

    def create_table(self):
        self.db.query(f"""
            CREATE TABLE IF NOT EXISTS {self.table} (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) UNIQUE NOT NULL
            )
        """)

    def save(self, store):
        self.db.query(f"""
            INSERT INTO {self.table} (id, name)
            VALUES (:id, :name)
            ON DUPLICATE KEY UPDATE  name = :name
        """, **vars(store))

        if not store.id:
            store.id = self.get(name=store.name).id
        return store

    def add_product(self, store, product):
        self.db.query("""
            INSERT IGNORE INTO product_store(product_id, store_id)
            VALUES (:product_id, :store_id)
        """, product_id=product.id, store_id=store.id)

    def get_all_by_product(self, product):
        stores = self.db.query(f"""
            SELECT store.id, store.name from store
            JOIN product_store ON product_store.store_id = store.id
            JOIN product ON product_store.product_id = product.id
            WHERE product.id = :id
        """, id=product.id).all(as_dict=True)
        return [self.model(**store) for store in stores]


class ProductRepository(Repository):

    table = 'product'

    def create_table(self):
        self.db.query(f"""
            CREATE TABLE IF NOT EXISTS {self.table} (
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

    def save(self, product):
        self.db.query(f"""
            INSERT INTO {self.table} (id, name)
            VALUES (:id, :name)
            ON DUPLICATE KEY UPDATE  name = :name
        """, **vars(product))

        return product

    def add_store(self, product, store):
        self.db.query("""
            INSERT IGNORE INTO product_store(product_id, store_id)
            VALUES (:product_id, :store_id)
        """, product_id=product.id, store_id=store.id)

    def get_all_by_store(self, store):
        products = self.db.query(f"""
            SELECT product.id, product.name from store
            JOIN product_store ON product_store.store_id = store.id
            JOIN product ON product_store.product_id = product.id
            WHERE store.id = :id
        """, id=store.id).all(as_dict=True)
        return [self.model(**product) for product in products]
