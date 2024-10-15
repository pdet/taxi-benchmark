import time
import statistics
import csv
import psutil
import duckdb
import os
import threading


script_dir = os.path.dirname(os.path.abspath(__file__))
schema_path = os.path.join(script_dir, 'sql' ,'schema.sql')

required_version = "1.1.1"
if duckdb.__version__ != required_version:
    raise ImportError(f"duckdb version {required_version} is required, but version {duckdb.__version__} is installed. Try `pip uninstall duckdb` and `pip install duckdb==1.1.1`")


# Function to monitor resource usage
def monitor_resource_usage(interval, cpu_usage_data, disk_usage_data, stop_event):
    while not stop_event.is_set():
        cpu_usage = psutil.cpu_percent(interval=None)
        disk_io = psutil.disk_io_counters()    
        cpu_usage_data.append(cpu_usage)
        disk_usage_data.append((disk_io.read_bytes, disk_io.write_bytes))
        time.sleep(interval)

# Run query, stores the time, and validate the results.
def run_query(conn, query_number):
    query_path = os.path.join(script_dir, 'sql','queries',f'q0{query_number}.sql')
    query_result = os.path.join(script_dir, 'sql','answers',f'q0{query_number}.csv')
    query_timer = []
    with open(query_path, 'r') as file:
        query_sql = file.read()
        # Validate result first
        result = conn.query(query_sql)
        answer = conn.read_csv(query_result)
        if query_number == '2':
            # We have to make the doubles prettier for comparisons
            result = conn.query('SELECT passenger_count, avg_total_amount::DECIMAL(15,3) FROM result')
            answer = conn.query('SELECT passenger_count, avg_total_amount::DECIMAL(15,3) FROM answer')
        if (len(answer.except_(result)) > 0 or len(result.except_(answer)) > 0):
            print("Query 0{query_number} failed")
            print("Answer except result:")
            print(answer.except_(result))
            print("Result except answer:")
            print(result.except_(answer))
            raise Exception("Query Result does not match with provided answer file. This benchmark is invalid!")
        for i in range (5):
            start_time = time.time()
            conn.execute(query_sql)
            end_time = time.time()
            query_timer.append(end_time - start_time)
    print(f"Query 0{query_number} executed in: " + str(statistics.median(query_timer)))


def benchmark(path, output_csv, monitoring_interval=1):
    decompressed_path = os.path.join(script_dir, 'data', path)
    decompressed_result = os.path.join(script_dir, 'data', output_csv)
    print (f"Running benchmark on: {decompressed_path}")
    load_times = []
    cpu_usage_data = []
    disk_usage_data = []
    for i in range(6): 
        conn = duckdb.connect()
        # Some settings for benchmarking
        conn.execute("PRAGMA max_temp_directory_size='1500GiB'")
        conn.execute("SET preserve_insertion_order = false")   
        # Loading the data, and capturing HW statistics on last run
        with open(schema_path, 'r') as file:
            create_sql = file.read()
        conn.execute(create_sql).fetchall()      
        load_query = f"COPY trips FROM '{decompressed_path}' (header 0);"
        start_time = time.time()     
        if i == 5:
            stop_event = threading.Event()
            monitor_thread = threading.Thread(target=monitor_resource_usage, args=(monitoring_interval, cpu_usage_data, disk_usage_data, stop_event))
            monitor_thread.start()
        conn.execute(load_query)
        end_time = time.time()
        if i < 5:
            load_times.append(end_time - start_time)
        else:
            stop_event.set()
            monitor_thread.join()
            # Run and validate benchmark queries
            for q in range (1,5):
                run_query(conn,str(q))
    print ("Load Time: " + str(statistics.median(load_times))) 
    
    # Write the resource usage data to CSV
    with open(decompressed_result, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['second', 'cpu_usage', 'disk_read', 'disk_write'])       
        for i in range(len(cpu_usage_data)):
            writer.writerow([i + 1, cpu_usage_data[i], disk_usage_data[i][0], disk_usage_data[i][1]])

benchmark('trips_x*.csv.gz', 'compressed_result.csv')
benchmark('decompressed.csv', 'decompressed_result.csv')

