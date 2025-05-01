SELECT
    c.region,
    AVG(t.amount) AS average_credit_transaction
FROM
    transactions t
JOIN
    customers c ON CAST(t.id AS BIGINT) = c.customer_id
WHERE
    t.transaction_type = 'C'
GROUP BY
    c.region
ORDER BY
    average_credit_transaction DESC;