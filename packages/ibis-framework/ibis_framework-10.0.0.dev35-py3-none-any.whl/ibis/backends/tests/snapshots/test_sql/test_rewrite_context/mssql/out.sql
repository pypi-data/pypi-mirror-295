SELECT
TOP 10
  NTILE(2) OVER (ORDER BY RAND() ASC) - 1 AS [new_col]
FROM [test] AS [t0]