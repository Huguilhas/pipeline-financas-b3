WITH base AS (
    SELECT
        date, 
        ticker,
        close,
        LAG(close) OVER(
            PARTITION BY ticker
            ORDER BY date
        ) AS close_anterior
    FROM {{ ref('stage_cotacoes') }}
)

SELECT 
    date,
    ticker,
    close,
    close_anterior,
    ROUND((close - close_anterior)/ close_anterior * 100,2) AS retorno_pct
FROM base
WHERE close_anterior IS NOT NULL