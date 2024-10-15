SELECT   passenger_count,
         DATE_PART('year', pickup_datetime) AS year,
         ROUND(trip_distance) AS distance,
         COUNT(*) AS count
FROM     trips
GROUP BY passenger_count,
         year,
         distance
ORDER BY year,
         count(*) DESC;