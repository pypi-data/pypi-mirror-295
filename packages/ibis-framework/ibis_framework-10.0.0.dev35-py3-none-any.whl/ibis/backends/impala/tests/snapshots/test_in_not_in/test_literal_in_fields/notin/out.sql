SELECT
  NOT (
    2 IN (`t0`.`a`, `t0`.`b`, `t0`.`c`)
  ) AS `Not(InValues(2, (a, b, c)))`
FROM `alltypes` AS `t0`