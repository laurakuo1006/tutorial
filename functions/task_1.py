import os
import csv
import random
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_1(folder="tutorial", output1="integers_a.csv", output2="integers_b.csv"):
    try:
        faasr_log("Starting task_1: generating random integer CSV files")

        os.makedirs("/tmp", exist_ok=True)

        random.seed(42)

        integers_a = [random.randint(1, 100) for _ in range(15)]
        integers_b = [random.randint(1, 100) for _ in range(15)]

        local_path_a = os.path.join("/tmp", output1)
        with open(local_path_a, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['value'])
            for val in integers_a:
                writer.writerow([val])

        faasr_log(f"Written local file {local_path_a} with 15 rows")

        local_path_b = os.path.join("/tmp", output2)
        with open(local_path_b, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['value'])
            for val in integers_b:
                writer.writerow([val])

        faasr_log(f"Written local file {local_path_b} with 15 rows")

        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)
        faasr_log(f"Uploaded {output1} to S3 folder {folder}")

        faasr_put_file(local_file=output2, remote_file=output2, local_folder="/tmp", remote_folder=folder)
        faasr_log(f"Uploaded {output2} to S3 folder {folder}")

        faasr_log("task_1 completed successfully: integers_a.csv and integers_b.csv uploaded")

    except Exception as e:
        faasr_log(f"Error in task_1: {str(e)}")
        raise

task_1("tutorial", "integers_a.csv", "integers_b.csv")