from pymongo import MongoClient
from cassandra.cluster import Cluster
from cassandra.io.asyncioreactor import AsyncioConnection
from cassandra.policies import AddressTranslator

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

client = MongoClient('mongodb://127.0.0.1:27017/', uuidRepresentation='standard')
db = client['ecommerce']

db.users.drop()
db.products.drop()
db.reviews.drop()
db.orders.drop()


users = [
    {
        "_id": r.user_id, 
        "name": r.name,
        "email": r.email,
        "created_at": r.created_at
    }
    for r in session.execute("SELECT user_id, name, email, created_at FROM users")
]

products = [
    {
        "_id": r.product_id,
        "name": r.name,
        "category": r.category,
        "price": r.price,
        "stock": r.stock
    }
    for r in session.execute("SELECT product_id, name, category, price, stock FROM products")
]

reviews = [
    {
        "_id": r.review_id,
        "product_id": r.product_id,
        "user_id": r.user_id,
        "user_name": r.user_name, # Terdenormalisasi dari Scylla
        "rating": r.rating,
        "comment": r.comment,
        "created_at": r.created_at
    }
    for r in session.execute(
        "SELECT review_id, product_id, user_id, user_name, rating, comment, created_at FROM reviews_by_product"
    )
]

orders = []
for r in session.execute(
    "SELECT user_id, created_at, order_id, total_amount, status, payment, items FROM orders_by_user"
):
    payment_doc = {
        "payment_id": r.payment.payment_id,
        "method": r.payment.method,
        "status": r.payment.status,
        "paid_at": r.payment.paid_at
    } if r.payment else None
    
    items_list = []
    if r.items:
        for it in r.items:
            items_list.append({
                "product_id": it.product_id,
                "name": it.product_name,
                "category": it.category,
                "qty": it.qty,
                "price": it.price
            })

    orders.append({
        "_id": r.order_id,
        "user_id": r.user_id,
        "created_at": r.created_at,
        "total_amount": r.total_amount,
        "status": r.status,
        "payment": payment_doc,
        "items": items_list
    })

print(f"   users={len(users)} products={len(products)} reviews={len(reviews)} orders={len(orders)}")

def insert_in_batches(collection, data, batch_size=10000):
    for i in range(0, len(data), batch_size):
        collection.insert_many(data[i:i+batch_size])

if users: insert_in_batches(db.users, users)
if products: insert_in_batches(db.products, products)
if reviews: insert_in_batches(db.reviews, reviews)
if orders: insert_in_batches(db.orders, orders)

expected = {
    "users": len(users), 
    "products": len(products), 
    "reviews": len(reviews),
    "orders": len(orders)
}

print("Migrasi selesai.")

client.close()
cluster.shutdown()