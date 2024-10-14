SELECT passenger_count, DATE_PART('year', pickup_datetime) AS year, COUNT(*) FROM trips GROUP BY passenger_count,year ORDER BY passenger_count,year;