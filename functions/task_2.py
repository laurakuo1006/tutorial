import os
import pandas as pd
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_2(folder="tutorial", input1="integers_a.csv", input2="integers_b.csv", output1="summed_results.csv"):
    try:
        os.makedirs("/tmp", exist_ok=True)

        faasr_log(f"Downloading {input1} from S3 folder {folder}")
        faasr_get_file(local_file=input1, remote_file=input1, local_folder="/tmp", remote_folder=folder)

        faasr_log(f"Downloading {input2} from S3 folder {folder}")
        faasr_get_file(local_file=input2, remote_file=input2, local_folder="/tmp", remote_folder=folder)

        path_a = os.path.join("/tmp", input1)
        path_b = os.path.join("/tmp", input2)
        path_out = os.path.join("/tmp", output1)

        faasr_log("Reading CSV files into DataFrames")
        df_a = pd.read_csv(path_a)
        df_b = pd.read_csv(path_b)

        # Sanity checks
        if len(df_a) != 15:
            raise ValueError(f"integers_a.csv must have exactly 15 data rows, found {len(df_a)}")
        if len(df_b) != 15:
            raise ValueError(f"integers_b.csv must have exactly 15 data rows, found {len(df_b)}")

        col_a = 'value_a'
        col_b = 'value_b'

        if col_a not in df_a.columns:
            raise ValueError(f"Column '{col_a}' not found in integers_a.csv")
        if col_b not in df_b.columns:
            raise ValueError(f"Column '{col_b}' not found in integers_b.csv")

        # Check for nulls
        if df_a[col_a].isnull().any():
            raise ValueError("integers_a.csv contains null values")
        if df_b[col_b].isnull().any():
            raise ValueError("integers_b.csv contains null values")

        # Check all values are whole integers (no floats)
        for val in df_a[col_a]:
            if not isinstance(val, (int,)) and not (isinstance(val, float) and val.is_integer()):
                raise ValueError(f"Non-integer value found in integers_a.csv: {val}")
            if isinstance(val, float) and not val.is_integer():
                raise ValueError(f"Float value found in integers_a.csv: {val}")

        for val in df_b[col_b]:
            if not isinstance(val, (int,)) and not (isinstance(val, float) and val.is_integer()):
                raise ValueError(f"Non-integer value found in integers_b.csv: {val}")
            if isinstance(val, float) and not val.is_integer():
                raise ValueError(f"Float value found in integers_b.csv: {val}")

        faasr_log("Validation passed. Converting to int and performing element-wise addition")

        # Convert to int to ensure no floats
        values_a = df_a[col_a].astype(int)
        values_b = df_b[col_b].astype(int)

        # Element-wise addition
        sums = values_a.values + values_b.values

        # Write output
        df_out = pd.DataFrame({'sum': sums.astype(int)})
        df_out.to_csv(path_out, index=False)
        faasr_log(f"Written {len(df_out)} rows to {path_out}")

        faasr_log(f"Uploading {output1} to S3 folder {folder}")
        faasr_put_file(local_file=output1, remote_file=output1, local_folder="/tmp", remote_folder=folder)
        faasr_log(f"Successfully uploaded {output1} to S3")

    except Exception as e:
        faasr_log(f"Error in task_2: {str(e)}")
        raise

task_2("tutorial", "integers_a.csv", "integers_b.csv", "summed_results.csv")