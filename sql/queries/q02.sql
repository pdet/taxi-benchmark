SELECT   passenger_count,
         AVG(total_amount) AS avg_total_amount
FROM     trips
GROUP BY passenger_count;