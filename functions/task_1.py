import os
import random
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_1(folder="tutorial", output1="integers_a.csv", output2="integers_b.csv"):
    try:
        faasr_log("Starting task_1: generating random integer CSV files")

        local_folder = "/tmp"
        os.makedirs(local_folder, exist_ok=True)

        path_a = os.path.join(local_folder, output1)
        path_b = os.path.join(local_folder, output2)

        integers_a = [random.randint(1, 100) for _ in range(10)]
        integers_b = [random.randint(1, 100) for _ in range(10)]

        faasr_log("Writing integers_a.csv to local temp folder")
        with open(path_a, 'w') as f:
            for val in integers_a:
                f.write(f"{val}\n")

        faasr_log("Writing integers_b.csv to local temp folder")
        with open(path_b, 'w') as f:
            for val in integers_b:
                f.write(f"{val}\n")

        # Verify each file contains exactly 10 rows
        with open(path_a, 'r') as f:
            rows_a = [line.strip() for line in f if line.strip()]
        with open(path_b, 'r') as f:
            rows_b = [line.strip() for line in f if line.strip()]

        assert len(rows_a) == 10, f"integers_a.csv has {len(rows_a)} rows, expected 10"
        assert len(rows_b) == 10, f"integers_b.csv has {len(rows_b)} rows, expected 10"

        faasr_log(f"integers_a.csv: {len(rows_a)} rows verified")
        faasr_log(f"integers_b.csv: {len(rows_b)} rows verified")

        faasr_log("Uploading integers_a.csv to S3")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder=local_folder, remote_folder=folder)

        faasr_log("Uploading integers_b.csv to S3")
        faasr_put_file(local_file=output2, remote_file=output2, local_folder=local_folder, remote_folder=folder)

        faasr_log("task_1 completed successfully: both CSV files uploaded to S3")

    except AssertionError as ae:
        faasr_log(f"Assertion error in task_1: {str(ae)}")
        raise
    except Exception as e:
        faasr_log(f"Error in task_1: {str(e)}")
        raise