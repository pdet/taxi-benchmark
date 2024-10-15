SELECT   passenger_count,
         DATE_PART('year', pickup_datetime) AS year,
         COUNT(*) AS count
FROM     trips
GROUP BY passenger_count,
         year;