SELECT
  `t2`.`c`,
  `t2`.`f`,
  `t2`.`foo_id`,
  `t2`.`bar_id`
FROM `star1` AS `t2`
CROSS JOIN `star2` AS `t3`