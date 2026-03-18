import os
import random
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_1(folder="tutorial", output1="input1.csv", output2="input2.csv"):
    try:
        faasr_log("Starting task_1: generating random values and writing to CSV files")

        os.makedirs("/tmp", exist_ok=True)

        random.seed(42)

        values1 = [random.randint(1, 100) for _ in range(10)]
        values2 = [random.randint(1, 100) for _ in range(10)]

        output1_local = os.path.join("/tmp", output1)
        faasr_log(f"Writing first CSV file to local path: {output1_local}")
        with open(output1_local, 'w') as f:
            for v in values1:
                f.write(f"{v}\n")

        output2_local = os.path.join("/tmp", output2)
        faasr_log(f"Writing second CSV file to local path: {output2_local}")
        with open(output2_local, 'w') as f:
            for v in values2:
                f.write(f"{v}\n")

        faasr_log(f"Uploading {output1} to S3 folder: {folder}")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Uploading {output2} to S3 folder: {folder}")
        faasr_put_file(local_file=output2, remote_file=output2, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Successfully written {output1} with values: {values1}")
        faasr_log(f"Successfully written {output2} with values: {values2}")
        faasr_log("task_1 completed successfully")

    except Exception as e:
        faasr_log(f"Error in task_1: {str(e)}")
        raise

task_1("tutorial", "input1.csv", "input2.csv")