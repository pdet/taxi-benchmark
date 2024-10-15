import pandas as pd
import matplotlib.pyplot as plt
import os
import duckdb

script_dir = os.path.dirname(os.path.abspath(__file__))


def analyse_benchmark(result_file, from_second = 90, to_second = 120): 
    con = duckdb.connect()

    path = os.path.join(script_dir,'data',result_file)
    deviation_below_100 = con.query(f"SELECT 100 - cpu_usage as deviation FROM '{path}' WHERE deviation > 0")
    average_deviation_below_100 = con.execute('SELECT sum(deviation)/count(*) FROM deviation_below_100').fetchone()

    print(f"Average deviation below 100%: {average_deviation_below_100[0]} %")

    duck_frame = con.query(f''' 
                SELECT cpu_usage,
                COALESCE(disk_read - LAG(disk_read) OVER (ORDER BY second), 0) AS disk_read_clean,
                COALESCE(disk_write - LAG(disk_write) OVER (ORDER BY second), 0) AS disk_write_clean,
                second
                FROM '{path}'
                WHERE second >= {from_second} AND second <= {to_second}
                ORDER BY second''')

    df = con.execute('''
            SELECT cpu_usage,
            second,
            disk_read_clean /(SELECT MAX(disk_read_clean) FROM duck_frame) * 100 as disk_read_percentage,
            disk_write_clean /(SELECT MAX(disk_write_clean) FROM duck_frame) * 100 as disk_write_percentage
            FROM duck_frame
        ''').df()
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(df["second"], df["cpu_usage"], marker='o', label='CPU Usage', color='blue')
    plt.plot(df["second"], df["disk_read_percentage"], marker='o', label='Disk Read (%)', color='green')
    plt.plot(df["second"], df["disk_write_percentage"], marker='o', label='Disk Write (%)', color='orange')
    plt.xlabel('Seconds')
    plt.ylabel('% Rates')
    plt.title('CPU Usage and Disk Read/Write Rates Over Time')
    plt.xticks(df["second"])  
    plt.legend()
    plt.grid()
    plt.show()

analyse_benchmark('compressed_result.csv')
analyse_benchmark('decompressed_result.csv')