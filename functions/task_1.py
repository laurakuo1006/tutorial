import os
import csv
import random
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_1(folder="tutorial", output1="file1.csv", output2="file2.csv"):
    try:
        local_folder = "/tmp"
        os.makedirs(local_folder, exist_ok=True)

        file1_path = os.path.join(local_folder, output1)
        file2_path = os.path.join(local_folder, output2)

        faasr_log("Generating random values for file1 and file2")
        values1 = [random.randint(1, 100) for _ in range(10)]
        values2 = [random.randint(1, 100) for _ in range(10)]

        faasr_log(f"Writing file1 to {file1_path}")
        with open(file1_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['value'])
            for v in values1:
                writer.writerow([v])

        faasr_log(f"Writing file2 to {file2_path}")
        with open(file2_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['value'])
            for v in values2:
                writer.writerow([v])

        faasr_log(f"Uploading {output1} to S3 folder {folder}")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder=local_folder, remote_folder=folder)

        faasr_log(f"Uploading {output2} to S3 folder {folder}")
        faasr_put_file(local_file=output2, remote_file=output2, local_folder=local_folder, remote_folder=folder)

        faasr_log(f"Created {output1} with values: {values1}")
        faasr_log(f"Created {output2} with values: {values2}")
        faasr_log("task_1 completed successfully")

    except Exception as e:
        faasr_log(f"Error in task_1: {str(e)}")
        raise