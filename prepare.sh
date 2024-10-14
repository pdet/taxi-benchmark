data_folder="data"
output_file="data/decompressed.csv"

> "$output_file"

for file in "$data_folder"/*.csv.gz; do
    gunzip -c "$file" >> "$output_file"
done