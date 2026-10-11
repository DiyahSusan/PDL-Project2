SELECT pr.category, SUM(oi.qty * oi.price)
FROM order_items oi
JOIN orders o ON o.order_id = oi.order_id
JOIN products pr ON pr.product_id = oi.product_id
GROUP BY pr.category;
