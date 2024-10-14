import os
import requests
import gzip
import shutil

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file_path = os.path.join(script_dir, 'files.txt')

output_path = os.path.join(script_dir, 'data')

os.makedirs(output_path, exist_ok=True)

def download_data():
    print("Downloading Data:")
    with open(input_file_path, 'r') as file:
        urls = file.readlines()
    for url in urls:
        url = url.strip()
        print (url)
        response = requests.get(url.strip(), stream=True)
        response.raise_for_status()
        filename = os.path.join(output_path, url.split('/')[-1])
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

def prepare_data():
    output_file =  os.path.join(output_path, 'decompressed.csv')
    with open(output_file, 'wb') as f:
        f.write(b'')
    for filename in os.listdir(output_path):
        if filename.endswith('.csv.gz'):
            gz_file_path = os.path.join(output_path, filename)
            with gzip.open(gz_file_path, 'rb') as gz_file:
                with open(output_file, 'ab') as out_file:
                    shutil.copyfileobj(gz_file, out_file)
            print(f"Decompressed: {gz_file_path}")

download_data()
prepare_data()