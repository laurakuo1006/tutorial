import os
import csv
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_2(folder="tutorial", input1="integers_a.csv", input2="integers_b.csv", output1="summed_results.csv"):
    try:
        os.makedirs("/tmp", exist_ok=True)

        local_a = "integers_a.csv"
        local_b = "integers_b.csv"
        local_out = "summed_results.csv"

        faasr_log("Downloading integers_a.csv from S3")
        faasr_get_file(local_file=local_a, remote_file=input1, local_folder="/tmp", remote_folder=folder)

        faasr_log("Downloading integers_b.csv from S3")
        faasr_get_file(local_file=local_b, remote_file=input2, local_folder="/tmp", remote_folder=folder)

        path_a = os.path.join("/tmp", local_a)
        path_b = os.path.join("/tmp", local_b)
        path_out = os.path.join("/tmp", local_out)

        faasr_log("Reading integers_a.csv")
        with open(path_a, newline='') as f:
            reader = csv.DictReader(f)
            rows_a = [int(row['value']) for row in reader]

        faasr_log("Reading integers_b.csv")
        with open(path_b, newline='') as f:
            reader = csv.DictReader(f)
            rows_b = [int(row['value']) for row in reader]

        if len(rows_a) != len(rows_b):
            faasr_log(f"Row count mismatch: integers_a.csv has {len(rows_a)} rows, integers_b.csv has {len(rows_b)} rows.")
            raise ValueError(f"Row count mismatch: integers_a.csv has {len(rows_a)} rows, integers_b.csv has {len(rows_b)} rows.")

        faasr_log("Computing element-wise sums")
        sums = [a + b for a, b in zip(rows_a, rows_b)]

        faasr_log("Writing summed_results.csv to /tmp")
        with open(path_out, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['sum'])
            for s in sums:
                writer.writerow([s])

        faasr_log(f"Written {len(sums)} summed rows to {path_out}")

        faasr_log("Uploading summed_results.csv to S3")
        faasr_put_file(local_file=local_out, remote_file=output1, local_folder="/tmp", remote_folder=folder)

        faasr_log("task_2 completed successfully")

    except Exception as e:
        faasr_log(f"Error in task_2: {str(e)}")
        raise