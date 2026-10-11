SELECT created_at, order_id, product_id, amount
FROM revenue_by_category
WHERE category = 'Elektronik'
  AND created_at >= '2026-10-01 00:00:00' 
  AND created_at <= '2026-10-31 23:59:59'
LIMIT 10;
