SELECT o.created_at, o.order_id, pr.name, (oi.qty * oi.price) AS total_revenue
FROM products pr
JOIN order_items oi ON pr.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE pr.category = 'Elektronik'
  AND o.created_at >= '2026-10-01 00:00:00'
  AND o.created_at <= '2026-10-31 23:59:59'
  AND o.status = 'COMPLETED'
ORDER BY o.created_at DESC
LIMIT 10;

