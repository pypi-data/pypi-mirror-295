SELECT
  ST_ASEWKB("t0"."<MULTIPOINT (10 40, 40 30, 20 20, 30 10)>") AS "<MULTIPOINT (10 40, 40 30, 20 20, 30 10)>"
FROM (
  SELECT
    ST_GEOMFROMTEXT('MULTIPOINT (10 40, 40 30, 20 20, 30 10)') AS "<MULTIPOINT (10 40, 40 30, 20 20, 30 10)>"
) AS "t0"