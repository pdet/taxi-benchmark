# Repository with Scripts to Run and Reproduce the Taxi Benchmark on DuckDB

## Requirements
We recommend at least 2 TB of available disk space to fully run this benchmark (including downloading and preparing the data). There is not necessarily a memory constraint limit; the theoretical minimum limit should be about 32 MB for each working thread. However, the more memory you have available and the more threads you use, the faster this benchmark will run.

### Bash Scripts
You will need `wget` and `gzip`.

### Python Scripts
You will need a Python 3 environment with pip installed. All necessary dependencies are listed in `python-dependencies.txt`.

## Download Files
To download the files, you simply have to run `./download.sh`. This will download the necessary 65 gzipped CSV files. Note that each file is approximately 1.8 GB, resulting in a total size of approximately 111 GB.

## Generate Uncompressed CSV File
This benchmark runs on the gzipped CSV files but can also run on the fully uncompressed data as one CSV file. This script uncompresses each file and combines them into one large file. Note that the size of this uncompressed file is approximately 630 GB. You can run this by executing `./prepare.sh`.

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
