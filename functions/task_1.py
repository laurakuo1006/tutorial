import os
import csv
import random
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_1(folder="tutorial", output1="integers_a.csv", output2="integers_b.csv"):
    try:
        faasr_log("Starting task_1: generating random integer CSV files")

        local_folder = "/tmp"
        os.makedirs(local_folder, exist_ok=True)

        random.seed(42)

        values_a = [random.randint(1, 100) for _ in range(15)]
        values_b = [random.randint(1, 100) for _ in range(15)]

        faasr_log(f"Generated {len(values_a)} values for {output1} and {len(values_b)} values for {output2}")

        path_a = os.path.join(local_folder, output1)
        with open(path_a, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['value'])
            for v in values_a:
                writer.writerow([v])

        faasr_log(f"Written local file {path_a}")

        path_b = os.path.join(local_folder, output2)
        with open(path_b, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['value'])
            for v in values_b:
                writer.writerow([v])

        faasr_log(f"Written local file {path_b}")

        faasr_put_file(local_file=output1, remote_file=output1, local_folder=local_folder, remote_folder=folder)
        faasr_log(f"Uploaded {output1} to S3 folder {folder}")

        faasr_put_file(local_file=output2, remote_file=output2, local_folder=local_folder, remote_folder=folder)
        faasr_log(f"Uploaded {output2} to S3 folder {folder}")

        faasr_log(f"task_1 completed successfully: uploaded {output1} and {output2} with 15 rows each to S3 folder {folder}")

    except Exception as e:
        faasr_log(f"Error in task_1: {str(e)}")
        raise

task_1("tutorial", "integers_a.csv", "integers_b.csv")