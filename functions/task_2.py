from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log
import os
import pandas as pd

def task_2(folder="tutorial", input1="integers_a.csv", input2="integers_b.csv", output1="sum_output.csv"):
    try:
        os.makedirs("/tmp", exist_ok=True)

        faasr_log(f"Downloading {input1} from S3 folder {folder}")
        faasr_get_file(local_file=input1, remote_file=input1, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Downloading {input2} from S3 folder {folder}")
        faasr_get_file(local_file=input2, remote_file=input2, local_folder="/tmp", remote_folder=folder)

        path_a = os.path.join("/tmp", input1)
        path_b = os.path.join("/tmp", input2)
        path_out = os.path.join("/tmp", output1)

        faasr_log(f"Reading {input1}")
        df_a = pd.read_csv(path_a)

        faasr_log(f"Reading {input2}")
        df_b = pd.read_csv(path_b)

        assert len(df_a) == 10, f"integers_a.csv does not contain exactly 10 rows (found {len(df_a)})"
        assert len(df_b) == 10, f"integers_b.csv does not contain exactly 10 rows (found {len(df_b)})"

        faasr_log("Computing element-wise sums")
        sums = df_a['value_a'].values + df_b['value_b'].values

        df_out = pd.DataFrame({'sum': sums.astype(int)})
        df_out.to_csv(path_out, index=False)

        faasr_log(f"Written {len(df_out)} rows to {path_out}, uploading to S3 folder {folder}")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Successfully uploaded {output1} to S3 folder {folder}")

    except AssertionError as ae:
        faasr_log(f"Assertion error in task_2: {str(ae)}")
        raise
    except Exception as e:
        faasr_log(f"Error in task_2: {str(e)}")
        raise