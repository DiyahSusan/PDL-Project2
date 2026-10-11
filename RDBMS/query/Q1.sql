SELECT 
    o.order_id, o.created_at, o.total_amount, o.status,
    pay.method, pay.status AS payment_status,
    json_agg(
        json_build_object('name', pr.name, 
        'category', pr.category, 'qty', oi.qty, 
        'price', oi.price)) AS items
FROM (
    SELECT * FROM orders 
    WHERE user_id = '1fb6b8aa-ecee-4847-a057-c694d0f7d5af' 
    ORDER BY created_at DESC LIMIT 10) o
JOIN payments pay ON pay.order_id = o.order_id
JOIN order_items oi ON oi.order_id  = o.order_id
JOIN products pr ON pr.product_id = oi.product_id
GROUP BY o.order_id, o.created_at, o.total_amount, o.status, pay.method, pay.status
ORDER BY o.created_at DESC;
