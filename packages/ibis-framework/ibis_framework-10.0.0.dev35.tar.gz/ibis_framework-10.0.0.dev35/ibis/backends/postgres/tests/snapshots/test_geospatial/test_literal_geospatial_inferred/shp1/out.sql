SELECT
  ST_ASEWKB("t0"."<POINT (1 1)>") AS "<POINT (1 1)>"
FROM (
  SELECT
    ST_GEOMFROMTEXT('POINT (1 1)') AS "<POINT (1 1)>"
) AS "t0"