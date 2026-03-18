from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log
import os
import csv
import random

def task_1(folder="tutorial", output1="random_integers_1.csv", output2="random_integers_2.csv"):
    try:
        local_folder = "/tmp"
        os.makedirs(local_folder, exist_ok=True)

        local_path1 = os.path.join(local_folder, output1)
        local_path2 = os.path.join(local_folder, output2)

        values1 = [random.randint(1, 100) for _ in range(10)]
        values2 = [random.randint(1, 100) for _ in range(10)]

        faasr_log(f"Generated values1: {values1}")
        with open(local_path1, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['value1'])
            for v in values1:
                writer.writerow([v])

        faasr_log(f"Generated values2: {values2}")
        with open(local_path2, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['value2'])
            for v in values2:
                writer.writerow([v])

        faasr_log(f"Uploading {output1} to S3 folder {folder}")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder=local_folder, remote_folder=folder)

        faasr_log(f"Uploading {output2} to S3 folder {folder}")
        faasr_put_file(local_file=output2, remote_file=output2, local_folder=local_folder, remote_folder=folder)

        faasr_log(f"task_1 completed successfully. Files uploaded: {output1}, {output2}")

    except Exception as e:
        faasr_log(f"Error in task_1: {str(e)}")
        raise

task_1("tutorial", "random_integers_1.csv", "random_integers_2.csv")