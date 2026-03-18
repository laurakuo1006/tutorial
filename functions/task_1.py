import os
import json
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_1(folder="tutorial", output1="config.json"):
    try:
        faasr_log("Starting task_1: generating configuration file")

        os.makedirs("/tmp", exist_ok=True)

        config = {
            "row_count": 15,
            "min_value": 1,
            "max_value": 100,
            "column_header": "value",
            "output_column_header": "sum"
        }

        local_output_path = os.path.join("/tmp", output1)
        with open(local_output_path, "w") as f:
            json.dump(config, f, indent=4)

        faasr_log(f"Configuration file written locally to: {local_output_path}")

        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Configuration file uploaded to S3 at: {folder}/{output1}")

    except Exception as e:
        faasr_log(f"Error in task_1: {str(e)}")
        raise

task_1("tutorial", "config.json")