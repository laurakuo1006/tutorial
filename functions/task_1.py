import os
import random
import csv
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_1(folder="tutorial", output1="integers_file1.csv", output2="integers_file2.csv"):
    try:
        os.makedirs("/tmp", exist_ok=True)

        local_path1 = os.path.join("/tmp", output1)
        local_path2 = os.path.join("/tmp", output2)

        integers1 = [random.randint(1, 100) for _ in range(10)]
        integers2 = [random.randint(1, 100) for _ in range(10)]

        faasr_log(f"Generated integers1: {integers1}")
        faasr_log(f"Generated integers2: {integers2}")

        with open(local_path1, 'w', newline='') as f:
            writer = csv.writer(f)
            for val in integers1:
                writer.writerow([val])

        faasr_log(f"Written local file: {local_path1}")

        with open(local_path2, 'w', newline='') as f:
            writer = csv.writer(f)
            for val in integers2:
                writer.writerow([val])

        faasr_log(f"Written local file: {local_path2}")

        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)
        faasr_log(f"Uploaded {output1} to S3 folder {folder}")

        faasr_put_file(local_file=output2, remote_file=output2, local_folder="/tmp", remote_folder=folder)
        faasr_log(f"Uploaded {output2} to S3 folder {folder}")

    except Exception as e:
        faasr_log(f"Error in task_1: {str(e)}")
        raise