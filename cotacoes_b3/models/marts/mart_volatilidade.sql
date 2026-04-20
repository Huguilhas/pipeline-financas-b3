SELECT
    ticker,
    MAX(retorno_pct)        AS retorno_maximo,
    MIN(retorno_pct)        AS retorno_minimo,
    STDDEV(retorno_pct)     AS volatilidade,
    AVG(retorno_pct)        AS retorno_medio
FROM {{ ref('mart_retorno_diario') }}
GROUP BY ticker