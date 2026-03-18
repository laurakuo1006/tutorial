import os
import csv
import random
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_1(folder="tutorial", output1="file1.csv", output2="file2.csv"):
    try:
        faasr_log("Starting task_1: generating two CSV files with random values")

        local_folder = "/tmp"
        os.makedirs(local_folder, exist_ok=True)

        output1_local = os.path.join(local_folder, output1)
        output2_local = os.path.join(local_folder, output2)

        random.seed(42)
        values1 = [random.randint(1, 100) for _ in range(10)]

        random.seed(99)
        values2 = [random.randint(1, 100) for _ in range(10)]

        faasr_log(f"Generated values for {output1}: {values1}")
        with open(output1_local, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['value'])
            for v in values1:
                writer.writerow([v])

        faasr_log(f"Generated values for {output2}: {values2}")
        with open(output2_local, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['value'])
            for v in values2:
                writer.writerow([v])

        faasr_log(f"Uploading {output1} to S3 folder '{folder}'")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder=local_folder, remote_folder=folder)

        faasr_log(f"Uploading {output2} to S3 folder '{folder}'")
        faasr_put_file(local_file=output2, remote_file=output2, local_folder=local_folder, remote_folder=folder)

        faasr_log("task_1 completed successfully: both CSV files uploaded to S3")

    except Exception as e:
        faasr_log(f"Error in task_1: {str(e)}")
        raise