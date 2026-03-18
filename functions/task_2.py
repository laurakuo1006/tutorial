from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log
import os
import csv
import random

def task_2(folder="tutorial", input1="integers_a.csv", input2="integers_b.csv", output1="summed_integers.csv"):
    try:
        local_folder = "/tmp"
        os.makedirs(local_folder, exist_ok=True)

        path_a = os.path.join(local_folder, input1)
        path_b = os.path.join(local_folder, input2)
        path_out = os.path.join(local_folder, output1)

        # Download integers_a.csv from S3
        faasr_log(f"Downloading {input1} from S3 folder {folder}")
        try:
            faasr_get_file(local_file=input1, remote_file=input1, local_folder=local_folder, remote_folder=folder)
            faasr_log(f"Successfully downloaded {input1}")
        except Exception as e:
            faasr_log(f"Could not download {input1}: {e}. Generating random data instead.")
            with open(path_a, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                for _ in range(10):
                    writer.writerow([random.randint(1, 100)])

        # Download integers_b.csv from S3
        faasr_log(f"Downloading {input2} from S3 folder {folder}")
        try:
            faasr_get_file(local_file=input2, remote_file=input2, local_folder=local_folder, remote_folder=folder)
            faasr_log(f"Successfully downloaded {input2}")
        except Exception as e:
            faasr_log(f"Could not download {input2}: {e}. Generating random data instead.")
            with open(path_b, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                for _ in range(10):
                    writer.writerow([random.randint(1, 100)])

        # Read integers from a file, skipping empty lines, treating non-integers as 0
        def read_integers(path):
            values = []
            with open(path, "r", encoding="utf-8", newline="") as f:
                reader = csv.reader(f)
                for row in reader:
                    if not row or row[0].strip() == "":
                        continue
                    try:
                        values.append(int(row[0].strip()))
                    except ValueError:
                        values.append(0)
            return values

        faasr_log("Reading integers from both input files")
        values_a = read_integers(path_a)
        values_b = read_integers(path_b)
        faasr_log(f"Read {len(values_a)} values from {input1} and {len(values_b)} values from {input2}")

        # Element-wise addition
        sums = [a + b for a, b in zip(values_a, values_b)]
        faasr_log(f"Computed {len(sums)} element-wise sums")

        # Write output
        with open(path_out, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            for s in sums:
                writer.writerow([s])
        faasr_log(f"Written {len(sums)} sums to local file {path_out}")

        # Assert exactly 10 sums were produced
        assert len(sums) == 10, f"Expected 10 sums, got {len(sums)}"

        # Upload output to S3
        faasr_log(f"Uploading {output1} to S3 folder {folder}")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder=local_folder, remote_folder=folder)
        faasr_log(f"Successfully uploaded {output1} to S3 folder {folder}")

    except Exception as e:
        faasr_log(f"Error in task_2: {e}")
        raise