SELECT
  CAST(CAST(`t0`.`i` AS TIMESTAMP) + INTERVAL 5 SECOND AS TIMESTAMP) AS `TimestampAdd(i, 5s)`
FROM `alltypes` AS `t0`