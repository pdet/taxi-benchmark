SELECT passenger_count, AVG(total_amount) as avg_total_amount FROM trips GROUP BY passenger_count order by passenger_count, avg_total_amount;