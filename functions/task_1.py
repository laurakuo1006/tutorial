import os
import random
import csv
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_1(folder="tutorial", output1="integers_a.csv", output2="integers_b.csv"):
    try:
        os.makedirs("/tmp", exist_ok=True)

        path_a = os.path.join("/tmp", output1)
        path_b = os.path.join("/tmp", output2)

        faasr_log("Generating random integer values for both output files.")

        values_a = [random.randint(1, 100) for _ in range(15)]
        values_b = [random.randint(1, 100) for _ in range(15)]

        faasr_log(f"Writing {output1} to /tmp.")
        with open(path_a, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['value_a'])
            for v in values_a:
                writer.writerow([v])

        faasr_log(f"Writing {output2} to /tmp.")
        with open(path_b, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['value_b'])
            for v in values_b:
                writer.writerow([v])

        faasr_log(f"Uploading {output1} to S3 folder '{folder}'.")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Uploading {output2} to S3 folder '{folder}'.")
        faasr_put_file(local_file=output2, remote_file=output2, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Successfully generated and uploaded {output1} and {output2} with 15 integer rows each.")

    except Exception as e:
        faasr_log(f"Error in task_1: {str(e)}")
        raise

task_1("tutorial", "integers_a.csv", "integers_b.csv")