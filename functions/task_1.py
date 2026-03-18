import os
import csv
import random
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_1(folder="tutorial", output1="integers_a.csv", output2="integers_b.csv"):
    try:
        faasr_log("Starting task_1: generating random integer CSV files")

        tmp_folder = "/tmp"
        os.makedirs(tmp_folder, exist_ok=True)

        path_a = os.path.join(tmp_folder, output1)
        path_b = os.path.join(tmp_folder, output2)

        values_a = [random.randint(1, 100) for _ in range(15)]
        values_b = [random.randint(1, 100) for _ in range(15)]

        faasr_log(f"Writing {output1} to local temp folder")
        with open(path_a, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['value'])
            for v in values_a:
                writer.writerow([v])

        faasr_log(f"Writing {output2} to local temp folder")
        with open(path_b, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['value'])
            for v in values_b:
                writer.writerow([v])

        faasr_log(f"Uploading {output1} to S3 folder '{folder}'")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder=tmp_folder, remote_folder=folder)

        faasr_log(f"Uploading {output2} to S3 folder '{folder}'")
        faasr_put_file(local_file=output2, remote_file=output2, local_folder=tmp_folder, remote_folder=folder)

        faasr_log(f"Successfully generated and uploaded {output1} and {output2} with 15 rows each")

    except Exception as e:
        faasr_log(f"Error in task_1: {str(e)}")
        raise