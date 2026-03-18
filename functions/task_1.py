import os
import random
import csv
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_1(folder="tutorial", output1="integers_a.csv", output2="integers_b.csv"):
    try:
        os.makedirs("/tmp", exist_ok=True)

        faasr_log("Starting task_1: generating random integers")

        def generate_integers(n=10, low=1, high=100):
            values = [random.randint(low, high) for _ in range(n)]
            assert len(values) == 10, "File must contain exactly 10 rows"
            assert all(low <= v <= high for v in values), "All values must be between 1 and 100"
            return values

        integers_a = generate_integers()
        integers_b = generate_integers()

        faasr_log(f"Generated integers_a: {integers_a}")
        faasr_log(f"Generated integers_b: {integers_b}")

        local_path_a = os.path.join("/tmp", output1)
        with open(local_path_a, 'w', newline='') as f:
            writer = csv.writer(f)
            for val in integers_a:
                writer.writerow([val])

        faasr_log(f"Written local file: {local_path_a}")

        local_path_b = os.path.join("/tmp", output2)
        with open(local_path_b, 'w', newline='') as f:
            writer = csv.writer(f)
            for val in integers_b:
                writer.writerow([val])

        faasr_log(f"Written local file: {local_path_b}")

        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)
        faasr_log(f"Uploaded {output1} to S3 folder {folder}")

        faasr_put_file(local_file=output2, remote_file=output2, local_folder="/tmp", remote_folder=folder)
        faasr_log(f"Uploaded {output2} to S3 folder {folder}")

        faasr_log("task_1 completed successfully")

    except Exception as e:
        faasr_log(f"Error in task_1: {str(e)}")
        raise