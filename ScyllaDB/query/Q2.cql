SELECT category, SUM(amount) 
FROM revenue_by_category 
GROUP BY category;

