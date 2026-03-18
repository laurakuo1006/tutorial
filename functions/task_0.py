import os
import numpy as np
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_0(folder="tutorial", output1="input1.csv", output2="input2.csv"):
    try:
        local_tmp = "/tmp"
        os.makedirs(local_tmp, exist_ok=True)

        faasr_log("Generating random data for input1.csv")
        np.random.seed(42)
        values1 = np.random.randint(1, 101, size=10)
        local_path1 = os.path.join(local_tmp, output1)
        with open(local_path1, 'w') as f:
            f.write("col1\n")
            for v in values1:
                f.write(f"{v}\n")

        faasr_log("Generating random data for input2.csv")
        np.random.seed(43)
        values2 = np.random.randint(1, 101, size=10)
        local_path2 = os.path.join(local_tmp, output2)
        with open(local_path2, 'w') as f:
            f.write("col2\n")
            for v in values2:
                f.write(f"{v}\n")

        faasr_log(f"Uploading {output1} to S3 folder {folder}")
        faasr_put_file(
            local_file=output1,
            remote_file=output1,
            local_folder=local_tmp,
            remote_folder=folder
        )

        faasr_log(f"Uploading {output2} to S3 folder {folder}")
        faasr_put_file(
            local_file=output2,
            remote_file=output2,
            local_folder=local_tmp,
            remote_folder=folder
        )

        faasr_log(f"Successfully written and uploaded {output1} and {output2} to S3 folder {folder}")

    except Exception as e:
        faasr_log(f"Error in task_0: {str(e)}")
        raise

task_0("tutorial", "input1.csv", "input2.csv")