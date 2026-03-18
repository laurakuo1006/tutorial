from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log
import os

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

        faasr_log("Reading values from both input files")
        with open(local_a, "r", encoding="utf-8") as f:
            values_a = [int(line.strip()) for line in f if line.strip()]

        with open(local_b, "r", encoding="utf-8") as f:
            values_b = [int(line.strip()) for line in f if line.strip()]

        faasr_log(f"Summing {len(values_a)} values from {input1} and {len(values_b)} values from {input2}")
        summed = [a + b for a, b in zip(values_a, values_b)]

        faasr_log(f"Writing {len(summed)} summed values to {local_out}")
        with open(local_out, "w", encoding="utf-8", newline="\n") as f:
            for val in summed:
                f.write(f"{val}\n")

        faasr_log(f"Uploading {output1} to S3 folder {folder}")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)

        faasr_log("task_2 completed successfully")

    except Exception as e:
        faasr_log(f"Error in task_2: {str(e)}")
        raise