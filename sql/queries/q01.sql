SELECT   cab_type,
         COUNT(*) AS count
FROM     trips
GROUP BY cab_type;