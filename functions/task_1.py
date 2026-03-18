import os
import random
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_1(folder="tutorial", output1="integers_a.csv", output2="integers_b.csv"):
    try:
        os.makedirs("/tmp", exist_ok=True)

        path_a = os.path.join("/tmp", output1)
        path_b = os.path.join("/tmp", output2)

        faasr_log("Generating random integers for two lists")

        integers_a = [random.randint(1, 100) for _ in range(10)]
        integers_b = [random.randint(1, 100) for _ in range(10)]

        faasr_log(f"Writing integers_a to local file: {path_a}")
        with open(path_a, 'w', encoding='utf-8') as f:
            for val in integers_a:
                f.write(f"{val}\n")

        faasr_log(f"Writing integers_b to local file: {path_b}")
        with open(path_b, 'w', encoding='utf-8') as f:
            for val in integers_b:
                f.write(f"{val}\n")

        faasr_log(f"Uploading {output1} to S3 folder {folder}")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Uploading {output2} to S3 folder {folder}")
        faasr_put_file(local_file=output2, remote_file=output2, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Successfully written {output1} with values: {integers_a}")
        faasr_log(f"Successfully written {output2} with values: {integers_b}")

    except Exception as e:
        faasr_log(f"Error in task_1: {str(e)}")
        raise