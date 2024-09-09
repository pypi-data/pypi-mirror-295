import os
import pandas as pd

def process_csv(input_path, output_dir, chunk_size):
    files = os.listdir(input_path)
    csv_file = [file for file in files if file.endswith('.csv')]
    
    if len(csv_file) != 1:
        raise ValueError("Expected exactly one CSV file in the folder")
    
    input_file = os.path.join(input_path, csv_file[0])
    output_name = os.path.splitext(csv_file[0])[0]
    
    chunks = pd.read_csv(input_file, chunksize=chunk_size)
    
    output_files_info = []
    
    for i, chunk in enumerate(chunks):
        output_file = os.path.join(output_dir, f'{output_name}_{i}.csv')
        chunk.to_csv(output_file, index=False)
        num_rows = len(chunk)
        output_files_info.append((output_file, num_rows))
    
    output_filename = 'output_files_info.txt'
    with open(os.path.join(output_dir, output_filename), 'w') as f:
        for filename, num_rows in output_files_info:
            f.write(f"{filename}: {num_rows}\n")
