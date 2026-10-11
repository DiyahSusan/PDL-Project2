SELECT u.name AS user_name, r.rating, r.comment, r.created_at
FROM reviews r
JOIN users u ON r.user_id = u.user_id
WHERE r.product_id = 'e3adbcd8-173d-4df6-a2d7-07bd16cd46ec'
ORDER BY r.created_at DESC
LIMIT 10;

