SELECT order_id, created_at, total_amount, payment, items
FROM orders_by_user
WHERE user_id = 1fb6b8aa-ecee-4847-a057-c694d0f7d5af
LIMIT 10;
