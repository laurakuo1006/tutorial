import os
import csv
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_2(folder="tutorial", input1="file1.csv", input2="file2.csv", output1="summed_output.csv"):
    try:
        os.makedirs("/tmp", exist_ok=True)

        faasr_log("Downloading input files from S3")
        faasr_get_file(local_file=input1, remote_file=input1, local_folder="/tmp", remote_folder=folder)
        faasr_get_file(local_file=input2, remote_file=input2, local_folder="/tmp", remote_folder=folder)

        input1_path = os.path.join("/tmp", input1)
        input2_path = os.path.join("/tmp", input2)
        output1_path = os.path.join("/tmp", output1)

        faasr_log(f"Reading values from {input1}")
        with open(input1_path, newline='') as f1:
            reader1 = csv.DictReader(f1)
            rows1 = [int(row['value']) for row in reader1]

        faasr_log(f"Reading values from {input2}")
        with open(input2_path, newline='') as f2:
            reader2 = csv.DictReader(f2)
            rows2 = [int(row['value']) for row in reader2]

        if len(rows1) != len(rows2):
            raise ValueError(f"Files have different numbers of data rows: {len(rows1)} vs {len(rows2)}")

        faasr_log(f"Summing {len(rows1)} rows from both files")
        sums = [v1 + v2 for v1, v2 in zip(rows1, rows2)]

        faasr_log(f"Writing {len(sums)} summed rows to {output1_path}")
        with open(output1_path, 'w', newline='') as fout:
            writer = csv.writer(fout)
            writer.writerow(['sum'])
            for s in sums:
                writer.writerow([s])

        faasr_log(f"Uploading output file {output1} to S3 folder {folder}")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"task_2 completed successfully: written {len(sums)} rows to {output1}")

    except Exception as e:
        faasr_log(f"Error in task_2: {str(e)}")
        raise