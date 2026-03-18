from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log
import os
import csv

def task_2(folder="tutorial", input1="integers_a.csv", input2="integers_b.csv", output1="summed_output.csv"):
    try:
        os.makedirs("/tmp", exist_ok=True)

        local_a = os.path.join("/tmp", input1)
        local_b = os.path.join("/tmp", input2)
        local_out = os.path.join("/tmp", output1)

        faasr_log(f"Downloading {input1} from S3 folder {folder}")
        faasr_get_file(local_file=input1, remote_file=input1, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Downloading {input2} from S3 folder {folder}")
        faasr_get_file(local_file=input2, remote_file=input2, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Reading {input1}")
        with open(local_a, "r", newline="") as f:
            reader = csv.reader(f)
            rows_a = [row for row in reader]

        faasr_log(f"Reading {input2}")
        with open(local_b, "r", newline="") as f:
            reader = csv.reader(f)
            rows_b = [row for row in reader]

        if len(rows_a) != len(rows_b):
            faasr_log(f"Error: Mismatched row counts: {len(rows_a)} vs {len(rows_b)}")
            raise ValueError(f"Mismatched row counts: {len(rows_a)} vs {len(rows_b)}")

        if len(rows_a) != 15:
            faasr_log(f"Error: Expected exactly 15 rows, but got {len(rows_a)}")
            raise ValueError(f"Expected exactly 15 rows, but got {len(rows_a)}")

        faasr_log("Computing row-wise sums")
        sums = []
        for i, (row_a, row_b) in enumerate(zip(rows_a, rows_b)):
            try:
                val_a = int(row_a[0].strip())
            except (ValueError, IndexError):
                faasr_log(f"Error: Non-integer value in {input1} at row {i}: {row_a}")
                raise ValueError(f"Non-integer value in {input1} at row {i}: {row_a}")
            try:
                val_b = int(row_b[0].strip())
            except (ValueError, IndexError):
                faasr_log(f"Error: Non-integer value in {input2} at row {i}: {row_b}")
                raise ValueError(f"Non-integer value in {input2} at row {i}: {row_b}")
            sums.append(val_a + val_b)

        faasr_log(f"Writing {len(sums)} summed rows to {local_out}")
        with open(local_out, "w", newline="") as f:
            writer = csv.writer(f)
            for s in sums:
                writer.writerow([s])

        faasr_log(f"Uploading {output1} to S3 folder {folder}")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"task_2 completed successfully: written {len(sums)} rows to {output1}")

    except Exception as e:
        faasr_log(f"task_2 encountered an error: {str(e)}")
        raise