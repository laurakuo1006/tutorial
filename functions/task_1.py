import os
import random
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_1(folder="tutorial", output1="file1.csv", output2="file2.csv"):
    try:
        faasr_log("Starting task_1: generating random CSV files")

        os.makedirs("/tmp", exist_ok=True)

        for output in [output1, output2]:
            local_path = os.path.join("/tmp", output)
            values = [random.randint(1, 100) for _ in range(10)]
            with open(local_path, 'w') as f:
                for v in values:
                    f.write(f"{v}\n")
            faasr_log(f"Generated local file: {local_path}")

            faasr_put_file(
                local_file=output,
                remote_file=output,
                local_folder="/tmp",
                remote_folder=folder
            )
            faasr_log(f"Uploaded {output} to S3 folder '{folder}'")

        faasr_log(f"Successfully generated and uploaded {output1} and {output2} to folder '{folder}'")

    except Exception as e:
        faasr_log(f"Error in task_1: {str(e)}")
        raise

task_1("tutorial", "file1.csv", "file2.csv")