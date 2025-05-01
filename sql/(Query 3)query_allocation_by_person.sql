SELECT
    t.id AS customer_id,
    t.period,
    c.region,
    t.currency,
    SUM(t.amount) AS total_allocation
FROM
    transactions t
JOIN
    customers c ON CAST(t.id AS BIGINT) = c.customer_id
GROUP BY
    t.id, t.period, c.region, t.currency
ORDER BY
    c.region, t.period, t.id;