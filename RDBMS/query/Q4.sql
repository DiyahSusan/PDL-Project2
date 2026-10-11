WITH ValidOrders AS (
    SELECT o.order_id, o.created_at, o.total_amount
    FROM orders o
    JOIN payments p ON o.order_id = p.order_id
    WHERE o.user_id = '1fb6b8aa-ecee-4847-a057-c694d0f7d5af'
      AND p.status = 'SUCCESS'
    ORDER BY o.created_at DESC
    LIMIT 5)
SELECT vo.order_id, vo.created_at, 
    vo.total_amount, SUM(oi.qty) AS total_items_bought,
    STRING_AGG(pr.name || ' (' || oi.qty || 'x)', ' | ') AS product_details
FROM ValidOrders vo
JOIN order_items oi ON vo.order_id = oi.order_id
JOIN products pr ON oi.product_id = pr.product_id
GROUP BY vo.order_id, vo.created_at, vo.total_amount
ORDER BY vo.created_at DESC;

