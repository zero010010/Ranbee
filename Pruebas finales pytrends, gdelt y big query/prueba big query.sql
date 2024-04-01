SELECT
  Date,
  V2Themes,
  Locations,
  Persons,
  Organizations
FROM
  `gdelt-bq.gdeltv2.gkg`
WHERE
  PARSE_TIMESTAMP('%Y%m%d%H%M%S', CAST(Date AS STRING)) BETWEEN TIMESTAMP('2024-01-01 00:00:00') AND TIMESTAMP('2024-03-25 23:59:59')
  AND LOWER(V2Themes) LIKE '%work%'
LIMIT 1000

