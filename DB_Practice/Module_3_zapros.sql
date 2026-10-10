SELECT oi.order_id,
       SUM(oi.quantity * s.qty * p.price) AS total_cost
FROM Order_items oi
JOIN Specification s ON s.product_id = oi.product_id
JOIN Prices p ON p.material_id = s.material_id
WHERE p.product_id IS NULL
GROUP BY oi.order_id;