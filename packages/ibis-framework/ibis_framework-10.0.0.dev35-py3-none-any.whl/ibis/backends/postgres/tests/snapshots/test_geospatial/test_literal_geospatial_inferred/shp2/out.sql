SELECT
  ST_ASEWKB("t0"."<POINT (2 2)>") AS "<POINT (2 2)>"
FROM (
  SELECT
    ST_GEOMFROMTEXT('POINT (2 2)') AS "<POINT (2 2)>"
) AS "t0"