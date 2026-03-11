from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log
import os
import csv

def task_2(folder="tutorial", input1="integers_a.csv", input2="integers_b.csv", output1="summed_integers.csv"):
    try:
        os.makedirs("/tmp", exist_ok=True)

        faasr_log(f"Downloading {input1} from S3 folder {folder}")
        faasr_get_file(local_file=input1, remote_file=input1, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Downloading {input2} from S3 folder {folder}")
        faasr_get_file(local_file=input2, remote_file=input2, local_folder="/tmp", remote_folder=folder)

        path_a = os.path.join("/tmp", input1)
        path_b = os.path.join("/tmp", input2)
        path_out = os.path.join("/tmp", output1)

        faasr_log(f"Reading values from {input1}")
        with open(path_a, "r", newline="") as f:
            reader = csv.reader(f)
            values_a = [int(row[0]) for row in reader]

        faasr_log(f"Reading values from {input2}")
        with open(path_b, "r", newline="") as f:
            reader = csv.reader(f)
            values_b = [int(row[0]) for row in reader]

        faasr_log(f"Summing {len(values_a)} values from {input1} and {len(values_b)} values from {input2}")
        summed = [a + b for a, b in zip(values_a, values_b)]

        faasr_log(f"Writing {len(summed)} summed values to {path_out}")
        with open(path_out, "w", newline="") as f:
            writer = csv.writer(f)
            for val in summed:
                writer.writerow([val])

        faasr_log(f"Uploading {output1} to S3 folder {folder}")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Successfully written {len(summed)} summed values to {output1}")

    except Exception as e:
        faasr_log(f"Error in task_2: {str(e)}")
        raise