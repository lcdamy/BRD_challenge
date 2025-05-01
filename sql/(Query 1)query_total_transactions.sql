SELECT
    id AS customer_id,
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_transaction_amount
FROM
    transactions
GROUP BY
    id
ORDER BY
    total_transaction_amount DESC;