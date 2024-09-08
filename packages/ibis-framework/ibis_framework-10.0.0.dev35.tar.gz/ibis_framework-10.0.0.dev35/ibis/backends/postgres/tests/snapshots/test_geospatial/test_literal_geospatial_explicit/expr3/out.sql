SELECT
  ST_ASEWKB("t0"."p") AS "p"
FROM (
  SELECT
    ST_GEOMFROMTEXT('POINT (1 1)', 4326) AS "p"
) AS "t0"