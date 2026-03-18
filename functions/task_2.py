from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log
import os
import csv

def task_2(folder="tutorial", input1="integers_a.csv", input2="integers_b.csv", output1="sums_output.csv"):
    try:
        os.makedirs("/tmp", exist_ok=True)

        faasr_log(f"Downloading input files '{input1}' and '{input2}' from S3 folder '{folder}'")
        faasr_get_file(local_file=input1, remote_file=input1, local_folder="/tmp", remote_folder=folder)
        faasr_get_file(local_file=input2, remote_file=input2, local_folder="/tmp", remote_folder=folder)

        input1_path = os.path.join("/tmp", input1)
        input2_path = os.path.join("/tmp", input2)
        output1_path = os.path.join("/tmp", output1)

        faasr_log(f"Reading '{input1_path}'")
        with open(input1_path, "r", newline="") as f:
            reader = csv.reader(f)
            values_a = [row for row in reader]

        faasr_log(f"Reading '{input2_path}'")
        with open(input2_path, "r", newline="") as f:
            reader = csv.reader(f)
            values_b = [row for row in reader]

        if len(values_a) != len(values_b):
            error_msg = (
                f"Row count mismatch: '{input1}' has {len(values_a)} rows, "
                f"'{input2}' has {len(values_b)} rows. Both must have the same number of rows."
            )
            faasr_log(error_msg)
            raise ValueError(error_msg)

        faasr_log(f"Computing sums for {len(values_a)} rows")
        sums = []
        for i, (row_a, row_b) in enumerate(zip(values_a, values_b)):
            val_a = int(row_a[0].strip())
            val_b = int(row_b[0].strip())
            sums.append(val_a + val_b)

        faasr_log(f"Writing {len(sums)} sums to '{output1_path}'")
        with open(output1_path, "w", newline="") as f:
            writer = csv.writer(f)
            for s in sums:
                writer.writerow([s])

        faasr_log(f"Uploading '{output1}' to S3 folder '{folder}'")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Successfully written {len(sums)} sums to '{output1}' in S3 folder '{folder}'.")

    except Exception as e:
        faasr_log(f"Error in task_2: {str(e)}")
        raise