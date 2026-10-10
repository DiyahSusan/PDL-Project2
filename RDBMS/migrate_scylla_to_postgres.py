import psycopg
from cassandra.cluster import Cluster
from cassandra.io.asyncioreactor import AsyncioConnection
from cassandra.policies import AddressTranslator

PG_DSN = "host=127.0.0.1 port=5433 dbname=ecommerce user=postgres password=postgres"

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
session.default_fetch_size = 2000
session.default_timeout = 120

pg = psycopg.connect(PG_DSN)

users = [
    (r.user_id, r.name, r.email, r.created_at)
    for r in session.execute("SELECT user_id, name, email, created_at FROM users")
]
products = [
    (r.product_id, r.name, r.category, r.price, r.stock)
    for r in session.execute("SELECT product_id, name, category, price, stock FROM products")
]
reviews = [
    (r.review_id, r.product_id, r.user_id, r.rating, r.comment, r.created_at)
    for r in session.execute(
        "SELECT review_id, product_id, user_id, rating, comment, created_at FROM reviews_by_product"
    )
]

orders, payments, order_items = [], [], []
for r in session.execute(
    "SELECT user_id, created_at, order_id, total_amount, status, payment, items FROM orders_by_user"
):
    orders.append((r.order_id, r.user_id, r.created_at, r.total_amount, r.status))
    p = r.payment
    payments.append((p.payment_id, r.order_id, p.method, p.status, p.paid_at))
    for it in r.items:
        order_items.append((r.order_id, it.product_id, it.qty, it.price))

print(f"   users={len(users)} products={len(products)} reviews={len(reviews)} "
      f"orders={len(orders)} payments={len(payments)} order_items={len(order_items)}")

def copy_rows(cur, target, rows):
    with cur.copy(f"COPY {target} FROM STDIN") as cp:
        for row in rows:
            cp.write_row(row)

with pg.cursor() as cur:
    copy_rows(cur, "users (user_id, name, email, created_at)", users)
    copy_rows(cur, "products (product_id, name, category, price, stock)", products)
    copy_rows(cur, "orders (order_id, user_id, created_at, total_amount, status)", orders)
    copy_rows(cur, "payments (payment_id, order_id, method, status, paid_at)", payments)
    copy_rows(cur, "order_items (order_id, product_id, qty, price)", order_items)
    copy_rows(cur, "reviews (review_id, product_id, user_id, rating, comment, created_at)", reviews)
pg.commit()

pg.execute("ANALYZE")
pg.commit()

expected = {
    "users": len(users), "products": len(products), "orders": len(orders),
    "payments": len(payments), "order_items": len(order_items), "reviews": len(reviews),
}

print("Migrasi selesai.")

pg.close()
cluster.shutdown()
