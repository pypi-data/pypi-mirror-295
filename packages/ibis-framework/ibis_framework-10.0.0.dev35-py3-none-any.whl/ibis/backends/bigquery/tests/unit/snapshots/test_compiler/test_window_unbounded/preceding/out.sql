SELECT
  SUM(`t0`.`a`) OVER (ROWS BETWEEN UNBOUNDED PRECEDING AND 1 preceding) AS `tmp`
FROM `t` AS `t0`