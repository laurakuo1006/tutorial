import os
import json
import random
import csv
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_2(folder="tutorial", input1="config.json", output1="integers_a.csv"):
    try:
        faasr_log("Starting task_2: downloading config file from S3")
        os.makedirs("/tmp", exist_ok=True)

        faasr_get_file(local_file=input1, remote_file=input1, local_folder="/tmp", remote_folder=folder)
        faasr_log(f"Downloaded {input1} from S3 folder {folder}")

        config_path = os.path.join("/tmp", input1)
        with open(config_path, 'r') as f:
            config = json.load(f)

        num_rows = config.get('num_rows', 15)
        min_val = config.get('min_val', 1)
        max_val = config.get('max_val', 100)
        seed = config.get('seed', None)

        faasr_log(f"Config loaded: num_rows={num_rows}, min_val={min_val}, max_val={max_val}, seed={seed}")

        if seed is not None:
            random.seed(seed)

        integers = [random.randint(min_val, max_val) for _ in range(num_rows)]

        output_path = os.path.join("/tmp", output1)
        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['value'])
            for val in integers:
                writer.writerow([val])

        faasr_log(f"Written {num_rows} integers to local file {output_path}")

        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)
        faasr_log(f"Uploaded {output1} to S3 folder {folder}")

    except Exception as e:
        faasr_log(f"Error in task_2: {str(e)}")
        raise