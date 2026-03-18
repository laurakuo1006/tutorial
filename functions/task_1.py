import os
import random
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_1(folder="tutorial", output1="integers_a.csv", output2="integers_b.csv"):
    try:
        os.makedirs("/tmp", exist_ok=True)

        local_path_a = os.path.join("/tmp", output1)
        local_path_b = os.path.join("/tmp", output2)

        faasr_log("Generating random integers for two lists")

        integers_a = [random.randint(1, 100) for _ in range(10)]
        integers_b = [random.randint(1, 100) for _ in range(10)]

        faasr_log(f"Writing integers_a to local file: {local_path_a}")
        with open(local_path_a, 'w') as f:
            for val in integers_a:
                f.write(f"{val}\n")

        faasr_log(f"Writing integers_b to local file: {local_path_b}")
        with open(local_path_b, 'w') as f:
            for val in integers_b:
                f.write(f"{val}\n")

        faasr_log(f"Uploading {output1} to S3 folder {folder}")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Uploading {output2} to S3 folder {folder}")
        faasr_put_file(local_file=output2, remote_file=output2, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Successfully uploaded {output1} with values: {integers_a}")
        faasr_log(f"Successfully uploaded {output2} with values: {integers_b}")

    except Exception as e:
        faasr_log(f"Error in task_1: {str(e)}")
        raise