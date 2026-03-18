from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log
import os
import csv

def task_2(folder="tutorial", input1="integers_file1.csv", input2="integers_file2.csv", output1="summed_output.csv"):
    try:
        os.makedirs("/tmp", exist_ok=True)

        local_input1 = os.path.join("/tmp", input1)
        local_input2 = os.path.join("/tmp", input2)
        local_output1 = os.path.join("/tmp", output1)

        faasr_log(f"Downloading {input1} from S3 folder {folder}")
        faasr_get_file(local_file=input1, remote_file=input1, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Downloading {input2} from S3 folder {folder}")
        faasr_get_file(local_file=input2, remote_file=input2, local_folder="/tmp", remote_folder=folder)

        # Read values from first CSV file
        with open(local_input1, 'r', newline='') as f1:
            reader1 = csv.reader(f1)
            rows1 = [row for row in reader1]

        # Read values from second CSV file
        with open(local_input2, 'r', newline='') as f2:
            reader2 = csv.reader(f2)
            rows2 = [row for row in reader2]

        # Detect if there's a header (non-numeric first row)
        def is_header(row):
            try:
                int(row[0])
                return False
            except (ValueError, IndexError):
                return True

        has_header1 = is_header(rows1[0]) if rows1 else False
        has_header2 = is_header(rows2[0]) if rows2 else False

        data1 = rows1[1:] if has_header1 else rows1
        data2 = rows2[1:] if has_header2 else rows2

        faasr_log(f"Performing element-wise addition on {len(data1)} rows")

        # Perform element-wise addition
        summed_rows = []
        for r1, r2 in zip(data1, data2):
            val1 = int(r1[0])
            val2 = int(r2[0])
            summed_rows.append([val1 + val2])

        # Write output CSV with no header row
        with open(local_output1, 'w', newline='') as fout:
            writer = csv.writer(fout)
            writer.writerows(summed_rows)

        faasr_log(f"Written {len(summed_rows)} rows to local file {local_output1}, uploading to S3 as {output1}")

        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Successfully uploaded {output1} to S3 folder {folder}")

    except Exception as e:
        faasr_log(f"Error in task_2: {str(e)}")
        raise