import os
import random
import csv
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_1(folder="tutorial", output1="file1.csv", output2="file2.csv"):
    try:
        faasr_log("Starting task_1: generating random CSV files")

        os.makedirs("/tmp", exist_ok=True)

        random.seed(42)

        values1 = [random.randint(1, 100) for _ in range(10)]
        values2 = [random.randint(1, 100) for _ in range(10)]

        output1_local = os.path.join("/tmp", output1)
        with open(output1_local, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['value'])
            for v in values1:
                writer.writerow([v])

        faasr_log(f"Generated local file {output1_local} with values: {values1}")

        output2_local = os.path.join("/tmp", output2)
        with open(output2_local, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['value'])
            for v in values2:
                writer.writerow([v])

        faasr_log(f"Generated local file {output2_local} with values: {values2}")

        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)
        faasr_log(f"Uploaded {output1} to S3 folder {folder}")

        faasr_put_file(local_file=output2, remote_file=output2, local_folder="/tmp", remote_folder=folder)
        faasr_log(f"Uploaded {output2} to S3 folder {folder}")

        faasr_log("task_1 completed successfully")

    except Exception as e:
        faasr_log(f"Error in task_1: {str(e)}")
        raise