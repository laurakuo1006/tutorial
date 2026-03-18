from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log
import os
import random

def task_1(folder="tutorial", output1="integers_a.csv", output2="integers_b.csv"):
    try:
        faasr_log("Starting task_1: generating random integers and uploading to S3")

        local_tmp = "/tmp"
        os.makedirs(local_tmp, exist_ok=True)

        local_path_a = os.path.join(local_tmp, output1)
        local_path_b = os.path.join(local_tmp, output2)

        integers_a = [random.randint(1, 100) for _ in range(10)]
        integers_b = [random.randint(1, 100) for _ in range(10)]

        faasr_log(f"Generated integers_a: {integers_a}")
        faasr_log(f"Generated integers_b: {integers_b}")

        with open(local_path_a, 'w') as f:
            for val in integers_a:
                f.write(f"{val}\n")

        with open(local_path_b, 'w') as f:
            for val in integers_b:
                f.write(f"{val}\n")

        faasr_log(f"Uploading {output1} to S3 folder {folder}")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder=local_tmp, remote_folder=folder)

        faasr_log(f"Uploading {output2} to S3 folder {folder}")
        faasr_put_file(local_file=output2, remote_file=output2, local_folder=local_tmp, remote_folder=folder)

        faasr_log("task_1 completed successfully")

    except Exception as e:
        faasr_log(f"Error in task_1: {str(e)}")
        raise