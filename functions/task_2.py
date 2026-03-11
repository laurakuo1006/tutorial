import os
import csv
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_2(folder="tutorial", input1="integers_a.csv", input2="integers_b.csv", output1="summed_results.csv"):
    try:
        os.makedirs("/tmp", exist_ok=True)

        faasr_log(f"Downloading {input1} from S3 folder {folder}")
        faasr_get_file(local_file=input1, remote_file=input1, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Downloading {input2} from S3 folder {folder}")
        faasr_get_file(local_file=input2, remote_file=input2, local_folder="/tmp", remote_folder=folder)

        path_a = os.path.join("/tmp", input1)
        path_b = os.path.join("/tmp", input2)
        path_out = os.path.join("/tmp", output1)

        faasr_log(f"Reading values from {input1}")
        with open(path_a, newline='') as f:
            reader = csv.DictReader(f)
            values_a = [int(row['value']) for row in reader]

        faasr_log(f"Reading values from {input2}")
        with open(path_b, newline='') as f:
            reader = csv.DictReader(f)
            values_b = [int(row['value']) for row in reader]

        if len(values_a) != len(values_b):
            faasr_log(f"Row count mismatch: {input1} has {len(values_a)} rows, {input2} has {len(values_b)} rows.")
            raise ValueError(f"Row count mismatch: {input1} has {len(values_a)} rows, {input2} has {len(values_b)} rows.")

        faasr_log(f"Computing element-wise sums for {len(values_a)} rows")
        sums = [a + b for a, b in zip(values_a, values_b)]

        faasr_log(f"Writing summed results to {path_out}")
        with open(path_out, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['sum'])
            for s in sums:
                writer.writerow([s])

        faasr_log(f"Uploading {output1} to S3 folder {folder}")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Successfully written {len(sums)} summed rows to {output1} in S3 folder {folder}")

    except Exception as e:
        faasr_log(f"Error in task_2: {str(e)}")
        raise