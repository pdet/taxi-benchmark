# Repository with Scripts to Run and Reproduce the Taxi Benchmark on DuckDB

## Requirements
We recommend at least 2 TB of available disk space to fully run this benchmark (including downloading and preparing the data). There is not necessarily a memory constraint limit; the theoretical minimum limit should be about 32 MB for each working thread. However, the more memory you have available and the more threads you use, the faster this benchmark will run.

### Python Scripts
You will need a Python 3 environment with pip installed. All necessary dependencies are listed in `requirements.txt`. You should be able to install it with `pip install -r requirements.txt`.

## Prepare dataset
To prepare the dataset, you need to download the necessary files, uncompress them, and combine them into a single CSV file. Both the uncompressed and compressed files are required to run this benchmark.
To download the necessary 65 gzipped CSV files and uncompress them, you will need approximately 650 GB of disk space.
This can be accomplished by executing `python generate_prepare_data.py`.

## Run Benchmark
The benchmark is depicted in the `benchmark.py` file and can be executed by running `python benchmark.py`.

The benchmark design can be broken down into two parts:
1. In the first part, we run the loader five consecutive times from scratch, store these times, and present the median time as the benchmarked time for the loader.
2. We then run it a sixth time, during which we capture resource information (e.g., CPU usage, disk writes/reads) instead of time. After this, we benchmark the queries in the `sql/queries` directory. Here, we also run each query five times and use the median time as the execution time. Note that we also validate that the query results are correct.

The script outputs the median loading times, the execution times of each query, and a CSV file with the resource details.

## Analyze Resource Files
The script used to analyze the files is in `analyse.py`. You can run it with `python analyse.py`. It calculates the deviation from 100% CPU usage and plots the CPU usage along with disk read/write metrics of the loader.

## Contributing
Of course, benchmarking is challenging, and it is possible that the scripts here can be improved. Feel free to open PRs with improvements or raise issues with any questions you might have.
