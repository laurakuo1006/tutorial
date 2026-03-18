import os
import csv
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_2(folder="tutorial", input1="integers_a.csv", input2="integers_b.csv", output1="summed_integers.csv"):
    try:
        os.makedirs("/tmp", exist_ok=True)

        local_path_a = os.path.join("/tmp", input1)
        local_path_b = os.path.join("/tmp", input2)
        local_path_out = os.path.join("/tmp", output1)

        faasr_log(f"Downloading {input1} from S3 folder {folder}")
        faasr_get_file(local_file=input1, remote_file=input1, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Downloading {input2} from S3 folder {folder}")
        faasr_get_file(local_file=input2, remote_file=input2, local_folder="/tmp", remote_folder=folder)

        def read_integers(path):
            values = []
            with open(path, newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    if not row:
                        continue
                    val_str = row[0].strip()
                    try:
                        val = int(val_str)
                    except ValueError:
                        raise ValueError(f"Non-integer value '{val_str}' found in {path}")
                    values.append(val)
            return values

        faasr_log(f"Reading integers from {local_path_a}")
        values_a = read_integers(local_path_a)

        faasr_log(f"Reading integers from {local_path_b}")
        values_b = read_integers(local_path_b)

        if len(values_a) != 10:
            raise ValueError(f"Expected 10 rows in {local_path_a}, but found {len(values_a)}")
        if len(values_b) != 10:
            raise ValueError(f"Expected 10 rows in {local_path_b}, but found {len(values_b)}")

        faasr_log("Computing element-wise sums")
        sums = []
        for a, b in zip(values_a, values_b):
            s = a + b
            if not (2 <= s <= 200):
                raise ValueError(f"Sum {s} is out of expected range [2, 200]")
            sums.append(s)

        faasr_log(f"Writing {len(sums)} summed values to {local_path_out}")
        with open(local_path_out, 'w', newline='') as f:
            writer = csv.writer(f)
            for s in sums:
                writer.writerow([s])

        faasr_log(f"Uploading {output1} to S3 folder {folder}")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Successfully written {len(sums)} summed values to {output1} in S3 folder {folder}")

    except Exception as e:
        faasr_log(f"Error in task_2: {str(e)}")
        raise