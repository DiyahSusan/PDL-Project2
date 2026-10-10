DROP TABLE IF EXISTS reviews, order_items, payments, orders, products, users CASCADE;

CREATE TABLE users (
    user_id    uuid PRIMARY KEY,
    name       text NOT NULL,
    email      text NOT NULL,
    created_at timestamp NOT NULL
);

CREATE TABLE products (
    product_id uuid PRIMARY KEY,
    name       text NOT NULL,
    category   text NOT NULL,
    price      bigint NOT NULL,
    stock      int NOT NULL CHECK (stock >= 0)
);

CREATE TABLE orders (
    order_id     uuid PRIMARY KEY,
    user_id      uuid NOT NULL REFERENCES users (user_id),
    created_at   timestamp NOT NULL,
    total_amount bigint NOT NULL,
    status       text NOT NULL            
);

CREATE TABLE payments (
    payment_id uuid PRIMARY KEY,
    order_id   uuid NOT NULL UNIQUE REFERENCES orders (order_id),
    method     text NOT NULL,
    status     text NOT NULL,             
    paid_at    timestamp NOT NULL
);

CREATE TABLE order_items (
    order_id   uuid NOT NULL REFERENCES orders (order_id),
    product_id uuid NOT NULL REFERENCES products (product_id),
    qty        int NOT NULL CHECK (qty > 0),
    price      bigint NOT NULL,           
    PRIMARY KEY (order_id, product_id)
);

CREATE TABLE reviews (
    review_id  uuid PRIMARY KEY,
    product_id uuid NOT NULL REFERENCES products (product_id),
    user_id    uuid NOT NULL REFERENCES users (user_id),
    rating     int NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment    text,
    created_at timestamp NOT NULL
);

-- indexing untuk menyetarakan dengan scylla
CREATE INDEX idx_orders_user_created   ON orders (user_id, created_at DESC);        
CREATE INDEX idx_reviews_product_created ON reviews (product_id, created_at DESC);  
CREATE INDEX idx_order_items_product   ON order_items (product_id);                
CREATE INDEX idx_products_category     ON products (category);                      