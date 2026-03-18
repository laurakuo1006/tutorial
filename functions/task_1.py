import os
import random
import csv
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_1(folder="tutorial", output1="integers_a.csv", output2="integers_b.csv"):
    try:
        faasr_log("Starting task_1: generating random integer CSV files")

        os.makedirs("/tmp", exist_ok=True)

        path_a = os.path.join("/tmp", output1)
        path_b = os.path.join("/tmp", output2)

        random.seed()

        integers_a = [random.randint(1, 100) for _ in range(15)]
        integers_b = [random.randint(1, 100) for _ in range(15)]

        faasr_log(f"Generated integers_a: {integers_a}")
        with open(path_a, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['value'])
            for val in integers_a:
                writer.writerow([val])

        faasr_log(f"Generated integers_b: {integers_b}")
        with open(path_b, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['value'])
            for val in integers_b:
                writer.writerow([val])

        faasr_log(f"Uploading {output1} to S3 folder {folder}")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Uploading {output2} to S3 folder {folder}")
        faasr_put_file(local_file=output2, remote_file=output2, local_folder="/tmp", remote_folder=folder)

        faasr_log("task_1 completed successfully")

    except Exception as e:
        faasr_log(f"Error in task_1: {str(e)}")
        raise