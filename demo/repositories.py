from zmodels import Repository

class StoreRepository(Repository):

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
