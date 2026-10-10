DROP KEYSPACE IF EXISTS ecommerce;

CREATE KEYSPACE ecommerce
WITH replication = {'class': 'NetworkTopologyStrategy', 'replication_factor': 1};

USE ecommerce;

CREATE TYPE payment_info (
    payment_id uuid,
    method     text,
    status     text,        
    paid_at    timestamp
);

CREATE TYPE order_item (
    product_id   uuid,
    product_name text,
    category     text,
    qty          int,
    price        bigint     
);

CREATE TABLE users (
    user_id    uuid PRIMARY KEY,
    name       text,
    email      text,
    created_at timestamp
);

CREATE TABLE products (
    product_id uuid PRIMARY KEY,
    name       text,
    category   text,
    price      bigint,
    stock      int
);

CREATE TABLE reviews_by_product (
    product_id uuid,
    created_at timestamp,
    review_id  uuid,
    user_id    uuid,
    user_name  text,
    rating     int,
    comment    text,
    PRIMARY KEY ((product_id), created_at, review_id)
) WITH CLUSTERING ORDER BY (created_at DESC, review_id ASC);

CREATE TABLE orders_by_user (
    user_id      uuid,
    created_at   timestamp,
    order_id     uuid,
    total_amount bigint,
    status       text,                         
    payment      frozen<payment_info>,
    items        list<frozen<order_item>>,
    PRIMARY KEY ((user_id), created_at, order_id)
) WITH CLUSTERING ORDER BY (created_at DESC, order_id ASC);

CREATE TABLE revenue_by_category (
    category   text,
    created_at timestamp,
    order_id   uuid,
    product_id uuid,
    amount     bigint,
    PRIMARY KEY ((category), created_at, order_id, product_id)
);