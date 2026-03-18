import os
import csv
import random
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_1(folder="tutorial", output1="integers_a.csv", output2="integers_b.csv"):
    try:
        os.makedirs("/tmp", exist_ok=True)

        path_a = os.path.join("/tmp", output1)
        path_b = os.path.join("/tmp", output2)

        faasr_log("Generating random integers for two CSV files.")

        integers_a = [random.randint(1, 100) for _ in range(15)]
        integers_b = [random.randint(1, 100) for _ in range(15)]

        with open(path_a, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['value_a'])
            for val in integers_a:
                writer.writerow([val])

        faasr_log(f"Written local file: {path_a}")

        with open(path_b, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['value_b'])
            for val in integers_b:
                writer.writerow([val])

        faasr_log(f"Written local file: {path_b}")

        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)
        faasr_log(f"Uploaded {output1} to S3 folder '{folder}'.")

        faasr_put_file(local_file=output2, remote_file=output2, local_folder="/tmp", remote_folder=folder)
        faasr_log(f"Uploaded {output2} to S3 folder '{folder}'.")

        faasr_log(f"Task complete: generated and uploaded {output1} and {output2} with 15 random integers each.")

    except Exception as e:
        faasr_log(f"Error in task_1: {str(e)}")
        raise

task_1("tutorial", "integers_a.csv", "integers_b.csv")