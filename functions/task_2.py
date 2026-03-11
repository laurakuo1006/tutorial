from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log
import os
import csv

def task_2(folder="tutorial", input1="input1.csv", input2="input2.csv", output1="output_sums.csv"):
    try:
        local_folder = "/tmp"
        os.makedirs(local_folder, exist_ok=True)

        faasr_log(f"Downloading {input1} from S3 folder {folder}")
        faasr_get_file(local_file=input1, remote_file=input1, local_folder=local_folder, remote_folder=folder)

        faasr_log(f"Downloading {input2} from S3 folder {folder}")
        faasr_get_file(local_file=input2, remote_file=input2, local_folder=local_folder, remote_folder=folder)

        input1_path = os.path.join(local_folder, input1)
        input2_path = os.path.join(local_folder, input2)
        output1_path = os.path.join(local_folder, output1)

        faasr_log(f"Reading values from {input1_path}")
        with open(input1_path, "r", newline="") as f1:
            reader1 = csv.reader(f1)
            values1 = [int(row[0]) for row in reader1]

        faasr_log(f"Reading values from {input2_path}")
        with open(input2_path, "r", newline="") as f2:
            reader2 = csv.reader(f2)
            values2 = [int(row[0]) for row in reader2]

        faasr_log(f"Computing element-wise sums for {len(values1)} rows")
        sums = [v1 + v2 for v1, v2 in zip(values1, values2)]

        faasr_log(f"Writing {len(sums)} rows to {output1_path}")
        with open(output1_path, "w", newline="") as fout:
            writer = csv.writer(fout)
            for s in sums:
                writer.writerow([s])

        faasr_log(f"Uploading {output1} to S3 folder {folder}")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder=local_folder, remote_folder=folder)

        faasr_log(f"Successfully written {len(sums)} rows to {output1} in S3 folder {folder}")

    except Exception as e:
        faasr_log(f"Error in task_2: {str(e)}")
        raise