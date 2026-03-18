import os
import random
import csv
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_1(folder="tutorial", output1="file1.csv", output2="file2.csv"):
    try:
        faasr_log("Starting task_1: generating random CSV files")

        local_tmp = "/tmp"
        os.makedirs(local_tmp, exist_ok=True)

        random.seed()

        # Generate 10 random integers for file1
        values1 = [random.randint(1, 100) for _ in range(10)]
        # Generate 10 random integers for file2
        values2 = [random.randint(1, 100) for _ in range(10)]

        faasr_log(f"Generated values for {output1}: {values1}")
        faasr_log(f"Generated values for {output2}: {values2}")

        # Write file1.csv to /tmp
        output1_local_path = os.path.join(local_tmp, output1)
        with open(output1_local_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for val in values1:
                writer.writerow([val])

        faasr_log(f"Written {output1} to local tmp: {output1_local_path}")

        # Write file2.csv to /tmp
        output2_local_path = os.path.join(local_tmp, output2)
        with open(output2_local_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for val in values2:
                writer.writerow([val])

        faasr_log(f"Written {output2} to local tmp: {output2_local_path}")

        # Upload file1.csv to S3
        faasr_log(f"Uploading {output1} to S3 folder '{folder}'")
        faasr_put_file(
            local_file=output1,
            remote_file=output1,
            local_folder=local_tmp,
            remote_folder=folder
        )
        faasr_log(f"Successfully uploaded {output1} to S3 folder '{folder}'")

        # Upload file2.csv to S3
        faasr_log(f"Uploading {output2} to S3 folder '{folder}'")
        faasr_put_file(
            local_file=output2,
            remote_file=output2,
            local_folder=local_tmp,
            remote_folder=folder
        )
        faasr_log(f"Successfully uploaded {output2} to S3 folder '{folder}'")

        faasr_log("task_1 completed successfully")

    except Exception as e:
        faasr_log(f"Error in task_1: {str(e)}")
        raise