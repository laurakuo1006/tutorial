import os
import csv
import random
from FaaSr_py.client.py_client_stubs import faasr_put_file, faasr_log

def task_1(folder="tutorial", output1="integers_a.csv", output2="integers_b.csv"):
    try:
        local_tmp = "/tmp"
        os.makedirs(local_tmp, exist_ok=True)

        local_path_a = os.path.join(local_tmp, output1)
        local_path_b = os.path.join(local_tmp, output2)

        faasr_log("Generating random integer values with seed 42")
        random.seed(42)
        values_a = [random.randint(1, 100) for _ in range(10)]
        values_b = [random.randint(1, 100) for _ in range(10)]

        faasr_log(f"Writing {output1} to local temp folder")
        with open(local_path_a, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['value'])
            for v in values_a:
                writer.writerow([v])

        faasr_log(f"Writing {output2} to local temp folder")
        with open(local_path_b, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['value'])
            for v in values_b:
                writer.writerow([v])

        faasr_log(f"Uploading {output1} to S3 folder '{folder}'")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder=local_tmp, remote_folder=folder)

        faasr_log(f"Uploading {output2} to S3 folder '{folder}'")
        faasr_put_file(local_file=output2, remote_file=output2, local_folder=local_tmp, remote_folder=folder)

        faasr_log(f"Successfully written {output1} with values: {values_a}")
        faasr_log(f"Successfully written {output2} with values: {values_b}")

    except Exception as e:
        faasr_log(f"Error in task_1: {str(e)}")
        raise