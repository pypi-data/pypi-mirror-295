SELECT
  *
  REPLACE (st_asbinary(`tmp`) AS `tmp`)
FROM (
  SELECT
    st_difference(`t0`.`geog0`, `t0`.`geog1`) AS `tmp`
  FROM `t` AS `t0`
)