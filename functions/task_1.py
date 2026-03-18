import os
import random
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_1(folder="tutorial", output1="integers_a.csv", output2="integers_b.csv"):
    try:
        faasr_log("Starting task_1: generating random integer CSV files")

        local_folder = "/tmp"
        os.makedirs(local_folder, exist_ok=True)

        local_path_a = os.path.join(local_folder, output1)
        local_path_b = os.path.join(local_folder, output2)

        random.seed()

        integers_a = [random.randint(1, 100) for _ in range(15)]
        integers_b = [random.randint(1, 100) for _ in range(15)]

        faasr_log(f"Generated integers_a: {integers_a}")
        faasr_log(f"Generated integers_b: {integers_b}")

        with open(local_path_a, 'w', encoding='utf-8') as f:
            for val in integers_a:
                f.write(f"{val}\n")

        faasr_log(f"Written local file: {local_path_a}")

        with open(local_path_b, 'w', encoding='utf-8') as f:
            for val in integers_b:
                f.write(f"{val}\n")

        faasr_log(f"Written local file: {local_path_b}")

        faasr_put_file(local_file=output1, remote_file=output1, local_folder=local_folder, remote_folder=folder)
        faasr_log(f"Uploaded {output1} to S3 folder {folder}")

        faasr_put_file(local_file=output2, remote_file=output2, local_folder=local_folder, remote_folder=folder)
        faasr_log(f"Uploaded {output2} to S3 folder {folder}")

        faasr_log("task_1 completed successfully")

    except Exception as e:
        faasr_log(f"Error in task_1: {str(e)}")
        raise