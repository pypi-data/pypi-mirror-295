SELECT
  *
FROM "t1" AS "t0"
WHERE
  EXISTS(
    SELECT
      1
    FROM "t2" AS "t1"
    WHERE
      "t0"."key1" = "t1"."key1"
  )