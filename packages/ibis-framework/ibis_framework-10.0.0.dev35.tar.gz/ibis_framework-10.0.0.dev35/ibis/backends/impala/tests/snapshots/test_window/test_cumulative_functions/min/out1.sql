SELECT
  MIN(`t0`.`f`) OVER (ORDER BY `t0`.`d` ASC) AS `foo`
FROM `alltypes` AS `t0`