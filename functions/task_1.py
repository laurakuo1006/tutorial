import os
import csv
import random
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_1(folder="tutorial", output1="integers_a.csv", output2="integers_b.csv"):
    try:
        os.makedirs("/tmp", exist_ok=True)

        local_path_a = os.path.join("/tmp", output1)
        local_path_b = os.path.join("/tmp", output2)

        faasr_log("Generating random integer lists for " + output1 + " and " + output2)

        values_a = [random.randint(1, 100) for _ in range(10)]
        values_b = [random.randint(1, 100) for _ in range(10)]

        with open(local_path_a, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['value_a'])
            for v in values_a:
                writer.writerow([v])

        faasr_log("Written local file: " + local_path_a)

        with open(local_path_b, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['value_b'])
            for v in values_b:
                writer.writerow([v])

        faasr_log("Written local file: " + local_path_b)

        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)
        faasr_log("Uploaded " + output1 + " to S3 folder: " + folder)

        faasr_put_file(local_file=output2, remote_file=output2, local_folder="/tmp", remote_folder=folder)
        faasr_log("Uploaded " + output2 + " to S3 folder: " + folder)

        faasr_log("task_1 completed successfully. Generated " + output1 + " and " + output2 + " with 10 random integers each (1-100).")

    except Exception as e:
        faasr_log("Error in task_1: " + str(e))
        raise

task_1("tutorial", "integers_a.csv", "integers_b.csv")