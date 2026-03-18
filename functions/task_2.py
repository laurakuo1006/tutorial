import os
import pandas as pd
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_2(folder="tutorial", input1="input1.csv", input2="input2.csv", output1="output_sums.csv"):
    try:
        os.makedirs("/tmp", exist_ok=True)

        local_input1 = os.path.join("/tmp", input1)
        local_input2 = os.path.join("/tmp", input2)
        local_output1 = os.path.join("/tmp", output1)

        faasr_log(f"Downloading {input1} from S3 folder '{folder}'")
        faasr_get_file(local_file=input1, remote_file=input1, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Downloading {input2} from S3 folder '{folder}'")
        faasr_get_file(local_file=input2, remote_file=input2, local_folder="/tmp", remote_folder=folder)

        faasr_log("Reading input CSV files into DataFrames")
        df1 = pd.read_csv(local_input1)
        df2 = pd.read_csv(local_input2)

        faasr_log(f"df1 shape: {df1.shape}, df2 shape: {df2.shape}")

        assert len(df1) == len(df2), f"Row count mismatch: {len(df1)} vs {len(df2)}"
        assert len(df1) == 10, f"Expected 10 rows, got {len(df1)}"

        faasr_log("Computing element-wise sums of 'value' columns")
        sums = df1['value'] + df2['value']
        result_df = pd.DataFrame({'sum': sums.astype(int)})

        faasr_log(f"Writing {len(result_df)} rows to local file {local_output1}")
        result_df.to_csv(local_output1, index=False)

        faasr_log(f"Uploading {output1} to S3 folder '{folder}'")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"task_2 completed successfully. Written {len(result_df)} rows to {output1}")

    except AssertionError as ae:
        faasr_log(f"Assertion error in task_2: {ae}")
        raise
    except Exception as e:
        faasr_log(f"Error in task_2: {e}")
        raise