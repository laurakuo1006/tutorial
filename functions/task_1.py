from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log
import os
import random

def task_1(folder="tutorial", output1="input1.csv", output2="input2.csv"):
    try:
        os.makedirs("/tmp", exist_ok=True)

        local_path1 = os.path.join("/tmp", output1)
        local_path2 = os.path.join("/tmp", output2)

        faasr_log(f"Generating random values for {output1} and {output2}")

        values1 = [random.randint(1, 100) for _ in range(10)]
        values2 = [random.randint(1, 100) for _ in range(10)]

        with open(local_path1, 'w') as f:
            for v in values1:
                f.write(f"{v}\n")

        faasr_log(f"Generated {local_path1} with values: {values1}")

        with open(local_path2, 'w') as f:
            for v in values2:
                f.write(f"{v}\n")

        faasr_log(f"Generated {local_path2} with values: {values2}")

        faasr_log(f"Uploading {output1} to S3 folder {folder}")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Uploading {output2} to S3 folder {folder}")
        faasr_put_file(local_file=output2, remote_file=output2, local_folder="/tmp", remote_folder=folder)

        faasr_log("task_1 completed successfully")

    except Exception as e:
        faasr_log(f"Error in task_1: {str(e)}")
        raise