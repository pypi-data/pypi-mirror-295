SELECT
  `t1`.`x`,
  `t1`.`y`
FROM (
  SELECT
    `t0`.`x`,
    SUM(`t0`.`x`) OVER (ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS `y`
  FROM `t` AS `t0`
) AS `t1`
WHERE
  `t1`.`y` <= 37
QUALIFY
  AVG(`t1`.`x`) OVER (ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) IS NOT NULL