import os
import csv
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_2(folder="tutorial", input1="integers_a.csv", input2="integers_b.csv", output1="summed_results.csv"):
    try:
        os.makedirs("/tmp", exist_ok=True)

        faasr_log(f"Downloading {input1} from S3 folder '{folder}'")
        faasr_get_file(local_file=input1, remote_file=input1, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Downloading {input2} from S3 folder '{folder}'")
        faasr_get_file(local_file=input2, remote_file=input2, local_folder="/tmp", remote_folder=folder)

        path_a = os.path.join("/tmp", input1)
        path_b = os.path.join("/tmp", input2)
        path_out = os.path.join("/tmp", output1)

        faasr_log(f"Reading {input1}")
        with open(path_a, newline='') as f:
            reader = csv.reader(f)
            header_a = next(reader)
            rows_a = [row for row in reader]

        faasr_log(f"Reading {input2}")
        with open(path_b, newline='') as f:
            reader = csv.reader(f)
            header_b = next(reader)
            rows_b = [row for row in reader]

        if len(rows_a) != len(rows_b):
            faasr_log(f"Row count mismatch: '{input1}' has {len(rows_a)} rows, '{input2}' has {len(rows_b)} rows.")
            raise ValueError(f"Row count mismatch: '{input1}' has {len(rows_a)} rows, '{input2}' has {len(rows_b)} rows.")

        faasr_log("Computing sums row by row")
        sums = []
        for row_a, row_b in zip(rows_a, rows_b):
            val_a = int(row_a[0])
            val_b = int(row_b[0])
            sums.append(val_a + val_b)

        faasr_log(f"Writing {len(sums)} summed rows to '{path_out}'")
        with open(path_out, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['sum'])
            for s in sums:
                writer.writerow([s])

        faasr_log(f"Uploading {output1} to S3 folder '{folder}'")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Successfully written {len(sums)} summed rows and uploaded '{output1}' to S3.")

    except Exception as e:
        faasr_log(f"Error in task_2: {str(e)}")
        raise