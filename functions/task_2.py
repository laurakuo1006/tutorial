import os
import csv
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_2(folder="tutorial", input1="integers_a.csv", input2="integers_b.csv", output1="summed_output.csv"):
    try:
        os.makedirs("/tmp", exist_ok=True)

        faasr_log(f"Downloading input files {input1} and {input2} from S3 folder {folder}")
        faasr_get_file(local_file=input1, remote_file=input1, local_folder="/tmp", remote_folder=folder)
        faasr_get_file(local_file=input2, remote_file=input2, local_folder="/tmp", remote_folder=folder)

        input1_path = os.path.join("/tmp", input1)
        input2_path = os.path.join("/tmp", input2)
        output1_path = os.path.join("/tmp", output1)

        faasr_log(f"Reading input files from /tmp")
        with open(input1_path, "r", newline="") as f1, open(input2_path, "r", newline="") as f2:
            reader1 = csv.DictReader(f1)
            reader2 = csv.DictReader(f2)

            rows1 = list(reader1)
            rows2 = list(reader2)

        min_len = min(len(rows1), len(rows2))
        faasr_log(f"Processing {min_len} rows from each input file")

        sums = []
        for i in range(min_len):
            val_a = int(rows1[i]["value"])
            val_b = int(rows2[i]["value"])
            sums.append(val_a + val_b)

        faasr_log(f"Writing {len(sums)} summed rows to {output1_path}")
        with open(output1_path, "w", newline="") as fout:
            writer = csv.writer(fout)
            writer.writerow(["sum"])
            for s in sums:
                writer.writerow([s])

        faasr_log(f"Uploading output file {output1} to S3 folder {folder}")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Successfully written {len(sums)} rows to {output1} in S3 folder {folder}")

    except Exception as e:
        faasr_log(f"Error in task_2: {str(e)}")
        raise