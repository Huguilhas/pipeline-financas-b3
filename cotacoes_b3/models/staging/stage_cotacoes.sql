{{ config(materialized='table') }}

WITH fonte AS (
    SELECT * FROM read_csv_auto(
        '{{ env_var("BRONZE_PATH", "../data/bronze") }}/*.csv',
        header = true
    )
)

SELECT  
    CAST(Date     AS DATE)        AS date,
    CAST(Ticker   AS VARCHAR)     AS ticker,
    CAST(Open     AS DECIMAL)     AS open,
    CAST(High     AS DECIMAL)     AS high,
    CAST(Low      AS DECIMAL)     AS low,
    CAST(Close    AS DECIMAL)     AS close,
    CAST(Volume   AS DECIMAL)     AS volume
FROM fonte