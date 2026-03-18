import os
import pandas as pd
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_2(folder="tutorial", input1="file1.csv", input2="file2.csv", output1="output.csv"):
    try:
        os.makedirs("/tmp", exist_ok=True)

        faasr_log(f"Downloading {input1} from S3 folder {folder}")
        faasr_get_file(local_file=input1, remote_file=input1, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Downloading {input2} from S3 folder {folder}")
        faasr_get_file(local_file=input2, remote_file=input2, local_folder="/tmp", remote_folder=folder)

        path1 = os.path.join("/tmp", input1)
        path2 = os.path.join("/tmp", input2)
        out_path = os.path.join("/tmp", output1)

        faasr_log(f"Reading {path1} and {path2}")
        df1 = pd.read_csv(path1)
        df2 = pd.read_csv(path2)

        if len(df1) != len(df2):
            faasr_log(f"Row count mismatch: file1 has {len(df1)} rows, file2 has {len(df2)} rows.")
            raise ValueError(f"Row count mismatch: file1 has {len(df1)} rows, file2 has {len(df2)} rows.")

        faasr_log("Computing sum of 'value' columns")
        result = pd.DataFrame({'sum': df1['value'].values + df2['value'].values})
        result['sum'] = result['sum'].astype(int)
        result.to_csv(out_path, index=False)
        faasr_log(f"Written {len(result)} rows to {out_path}")

        faasr_log(f"Uploading {output1} to S3 folder {folder}")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)
        faasr_log(f"Successfully uploaded {output1} to S3 folder {folder}")

    except Exception as e:
        faasr_log(f"Error in task_2: {str(e)}")
        raise