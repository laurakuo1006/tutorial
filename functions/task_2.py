import os
import csv
import random
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_2(folder="tutorial", input1="input1.csv", input2="input2.csv", output1="output_sums.csv"):
    try:
        os.makedirs("/tmp", exist_ok=True)

        input1_local = os.path.join("/tmp", input1)
        input2_local = os.path.join("/tmp", input2)
        output1_local = os.path.join("/tmp", output1)

        # Download input1.csv from S3
        faasr_log(f"Downloading {input1} from S3 folder {folder}")
        try:
            faasr_get_file(local_file=input1, remote_file=input1, local_folder="/tmp", remote_folder=folder)
            faasr_log(f"Successfully downloaded {input1}")
        except Exception as e:
            faasr_log(f"Could not download {input1} from S3, generating random data: {e}")
            with open(input1_local, 'w', newline='') as f:
                writer = csv.writer(f)
                for _ in range(10):
                    writer.writerow([random.randint(1, 100)])

        # Download input2.csv from S3
        faasr_log(f"Downloading {input2} from S3 folder {folder}")
        try:
            faasr_get_file(local_file=input2, remote_file=input2, local_folder="/tmp", remote_folder=folder)
            faasr_log(f"Successfully downloaded {input2}")
        except Exception as e:
            faasr_log(f"Could not download {input2} from S3, generating random data: {e}")
            with open(input2_local, 'w', newline='') as f:
                writer = csv.writer(f)
                for _ in range(10):
                    writer.writerow([random.randint(1, 100)])

        # Read input1.csv
        faasr_log(f"Reading {input1_local}")
        values1 = []
        with open(input1_local, 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                values1.append(int(row[0]))

        # Read input2.csv
        faasr_log(f"Reading {input2_local}")
        values2 = []
        with open(input2_local, 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                values2.append(int(row[0]))

        # Element-wise addition
        faasr_log("Performing element-wise addition")
        sums = [v1 + v2 for v1, v2 in zip(values1, values2)]

        # Write output_sums.csv to /tmp
        faasr_log(f"Writing {len(sums)} sums to {output1_local}")
        with open(output1_local, 'w', newline='') as f:
            writer = csv.writer(f)
            for s in sums:
                writer.writerow([int(s)])

        # Upload output_sums.csv to S3
        faasr_log(f"Uploading {output1} to S3 folder {folder}")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)
        faasr_log(f"Successfully uploaded {output1} to S3 folder {folder}")

    except Exception as e:
        faasr_log(f"Error in task_2: {e}")
        raise