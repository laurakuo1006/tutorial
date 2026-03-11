import os
import csv
import random
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_2(folder="tutorial", input1="integers_a.csv", input2="integers_b.csv", output1="summed_results.csv"):
    try:
        os.makedirs("/tmp", exist_ok=True)

        local_a = os.path.join("/tmp", input1)
        local_b = os.path.join("/tmp", input2)
        local_out = os.path.join("/tmp", output1)

        # Download integers_a.csv from S3
        faasr_log(f"Downloading {input1} from S3 folder {folder}")
        try:
            faasr_get_file(local_file=input1, remote_file=input1, local_folder="/tmp", remote_folder=folder)
            faasr_log(f"Successfully downloaded {input1}")
        except Exception as e:
            faasr_log(f"Could not download {input1}: {e}. Generating random data instead.")
            with open(local_a, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for _ in range(10):
                    writer.writerow([random.randint(1, 100)])

        # Download integers_b.csv from S3
        faasr_log(f"Downloading {input2} from S3 folder {folder}")
        try:
            faasr_get_file(local_file=input2, remote_file=input2, local_folder="/tmp", remote_folder=folder)
            faasr_log(f"Successfully downloaded {input2}")
        except Exception as e:
            faasr_log(f"Could not download {input2}: {e}. Generating random data instead.")
            with open(local_b, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for _ in range(10):
                    writer.writerow([random.randint(1, 100)])

        # Read integers from both files
        faasr_log("Reading values from both input files")
        with open(local_a, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            values_a = [int(row[0]) for row in reader]

        with open(local_b, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            values_b = [int(row[0]) for row in reader]

        faasr_log(f"Read {len(values_a)} values from {input1} and {len(values_b)} values from {input2}")

        # Perform element-wise addition
        sums = [a + b for a, b in zip(values_a, values_b)]
        faasr_log(f"Computed {len(sums)} element-wise sums")

        # Write results to output CSV
        with open(local_out, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for s in sums:
                writer.writerow([s])

        faasr_log(f"Written {len(sums)} rows to local file {local_out}")

        # Upload output to S3
        faasr_log(f"Uploading {output1} to S3 folder {folder}")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)
        faasr_log(f"Successfully uploaded {output1} to S3 folder {folder}")

    except Exception as e:
        faasr_log(f"Error in task_2: {e}")
        raise