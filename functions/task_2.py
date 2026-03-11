import os
import csv
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_2(folder="tutorial", input1="integers_a.csv", input2="integers_b.csv", output1="summed_results.csv"):
    try:
        os.makedirs("/tmp", exist_ok=True)

        faasr_log(f"Downloading input files '{input1}' and '{input2}' from S3 folder '{folder}'.")
        faasr_get_file(local_file=input1, remote_file=input1, local_folder="/tmp", remote_folder=folder)
        faasr_get_file(local_file=input2, remote_file=input2, local_folder="/tmp", remote_folder=folder)

        input1_path = os.path.join("/tmp", input1)
        input2_path = os.path.join("/tmp", input2)
        output1_path = os.path.join("/tmp", output1)

        faasr_log(f"Reading '{input1_path}'.")
        with open(input1_path, "r", newline="") as f:
            reader = csv.reader(f)
            rows_a = list(reader)

        faasr_log(f"Reading '{input2_path}'.")
        with open(input2_path, "r", newline="") as f:
            reader = csv.reader(f)
            rows_b = list(reader)

        if len(rows_a) != len(rows_b):
            faasr_log(f"Row count mismatch: 'integers_a.csv' has {len(rows_a)} rows, 'integers_b.csv' has {len(rows_b)} rows.")
            raise ValueError(f"Row count mismatch: 'integers_a.csv' has {len(rows_a)} rows, 'integers_b.csv' has {len(rows_b)} rows.")

        if len(rows_a) != 10:
            faasr_log(f"Expected exactly 10 rows, but found {len(rows_a)} rows.")
            raise ValueError(f"Expected exactly 10 rows, but found {len(rows_a)} rows.")

        faasr_log("Computing element-wise sums.")
        sums = []
        for row_a, row_b in zip(rows_a, rows_b):
            val_a = int(row_a[0])
            val_b = int(row_b[0])
            sums.append(val_a + val_b)

        faasr_log(f"Writing {len(sums)} summed results to '{output1_path}'.")
        with open(output1_path, "w", newline="") as f:
            writer = csv.writer(f)
            for s in sums:
                writer.writerow([s])

        faasr_log(f"Uploading '{output1}' to S3 folder '{folder}'.")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Successfully written {len(sums)} summed results and uploaded '{output1}' to S3.")

    except Exception as e:
        faasr_log(f"Error in task_2: {e}")
        raise