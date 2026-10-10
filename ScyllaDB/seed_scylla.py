import uuid
import random
from cassandra.cluster import Cluster
from cassandra.io.asyncioreactor import AsyncioConnection
from cassandra.concurrent import execute_concurrent_with_args
from cassandra.policies import AddressTranslator
from faker import Faker

fake = Faker('id_ID')

class LocalhostTranslator(AddressTranslator):
    def translate(self, addr):
        return '127.0.0.1'

cluster = Cluster(
    ['127.0.0.1'],
    port=9042,
    connection_class=AsyncioConnection,
    address_translator=LocalhostTranslator(),
)
session = cluster.connect('ecommerce')

categories = ['Elektronik', 'Pakaian', 'Buku', 'Kecantikan', 'Otomotif']
statuses = ['PAID', 'SHIPPED', 'COMPLETED', 'CANCELLED']
statuses_weights = [20, 25, 45, 10]
methods = ['CREDIT_CARD', 'BANK_TRANSFER', 'E_WALLET']

users = [
    {'id': uuid.uuid4(), 'name': fake.name(), 'email': fake.unique.email()}
    for _ in range(5000)
]
user_stmt = session.prepare(
    "INSERT INTO users (user_id, name, email, created_at) VALUES (?, ?, ?, ?)"
)
execute_concurrent_with_args(
    session, user_stmt,
    [(u['id'], u['name'], u['email'], fake.date_time_this_year()) for u in users],
    concurrency=100,
)
print("5.000 Users berhasil dibuat.")

products = [
    {
        'id': uuid.uuid4(),
        'name': fake.catch_phrase(),
        'category': random.choice(categories),
        'price': int(round(random.uniform(10000, 2000000), -3)),
        'stock': random.randint(10, 500),
    }
    for _ in range(1000)
]
product_stmt = session.prepare(
    "INSERT INTO products (product_id, name, category, price, stock) VALUES (?, ?, ?, ?, ?)"
)
execute_concurrent_with_args(
    session, product_stmt,
    [(p['id'], p['name'], p['category'], p['price'], p['stock']) for p in products],
    concurrency=100,
)
print("1.000 Produk berhasil dibuat.")

review_stmt = session.prepare("""
    INSERT INTO reviews_by_product (product_id, created_at, review_id, user_id, user_name, rating, comment)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""")
review_params = []
for _ in range(50000):
    u = random.choice(users)
    p = random.choice(products)
    review_params.append((
        p['id'], fake.date_time_this_year(), uuid.uuid4(),
        u['id'], u['name'], random.randint(1, 5), fake.sentence(),
    ))
execute_concurrent_with_args(session, review_stmt, review_params, concurrency=100)
print("50.000 Reviews berhasil dibuat.")

order_stmt = session.prepare("""
    INSERT INTO orders_by_user (user_id, created_at, order_id, total_amount, status, payment, items)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""")
revenue_stmt = session.prepare("""
    INSERT INTO revenue_by_category (category, created_at, order_id, product_id, amount)
    VALUES (?, ?, ?, ?, ?)
""")

order_params = []
revenue_params = []

for _ in range(50000):
    u = random.choice(users)
    oid = uuid.uuid4()
    created = fake.date_time_this_year()
    status = random.choices(statuses, weights=statuses_weights)[0]

    chosen = random.sample(products, random.randint(1, 4))
    items = []
    total = 0
    for p in chosen:
        qty = random.randint(1, 3)
        total += qty * p['price']
        items.append((p['id'], p['name'], p['category'], qty, p['price']))
        if status != 'CANCELLED':
            revenue_params.append((p['category'], created, oid, p['id'], qty * p['price']))

    pay_status = random.choice(['FAILED', 'REFUNDED']) if status == 'CANCELLED' else 'SUCCESS'
    payment = (uuid.uuid4(), random.choice(methods), pay_status, created)

    order_params.append((u['id'], created, oid, total, status, payment, items))


execute_concurrent_with_args(session, order_stmt, order_params, concurrency=100)
print("50.000 Orders berhasil dibuat.")

execute_concurrent_with_args(session, revenue_stmt, revenue_params, concurrency=100)
print(f"{len(revenue_params):,} Revenue Records berhasil dibuat.")

print("Seeding Selesai!")
cluster.shutdown()
