import os
import csv
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_3(folder="tutorial", input1="summed_output.csv", input2="integers_a.csv", input3="integers_b.csv", output1="element_wise_addition_validation_report.txt"):
    try:
        local_tmp = "/tmp"
        os.makedirs(local_tmp, exist_ok=True)

        faasr_log(f"Downloading input files from S3 folder '{folder}'")

        try:
            faasr_get_file(local_file=input1, remote_file=input1, local_folder=local_tmp, remote_folder=folder)
            faasr_log(f"Downloaded '{input1}' successfully.")
        except Exception as e:
            faasr_log(f"ERROR: Could not download '{input1}': {e}")

        try:
            faasr_get_file(local_file=input2, remote_file=input2, local_folder=local_tmp, remote_folder=folder)
            faasr_log(f"Downloaded '{input2}' successfully.")
        except Exception as e:
            faasr_log(f"ERROR: Could not download '{input2}': {e}")

        try:
            faasr_get_file(local_file=input3, remote_file=input3, local_folder=local_tmp, remote_folder=folder)
            faasr_log(f"Downloaded '{input3}' successfully.")
        except Exception as e:
            faasr_log(f"ERROR: Could not download '{input3}': {e}")

        summed_path = os.path.join(local_tmp, input1)
        integers_a_path = os.path.join(local_tmp, input2)
        integers_b_path = os.path.join(local_tmp, input3)
        report_path = os.path.join(local_tmp, output1)

        discrepancies = []
        results = []

        def read_single_column_csv(filepath):
            rows = []
            with open(filepath, 'r', newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    rows.append(row)
            return rows

        faasr_log("Reading input CSV files")

        try:
            summed_rows = read_single_column_csv(summed_path)
        except Exception as e:
            discrepancies.append(f"ERROR: Could not read '{input1}': {e}")
            summed_rows = []

        try:
            a_rows = read_single_column_csv(integers_a_path)
        except Exception as e:
            discrepancies.append(f"ERROR: Could not read '{input2}': {e}")
            a_rows = []

        try:
            b_rows = read_single_column_csv(integers_b_path)
        except Exception as e:
            discrepancies.append(f"ERROR: Could not read '{input3}': {e}")
            b_rows = []

        faasr_log("Checking row count of summed_output.csv")
        num_summed_rows = len(summed_rows)
        if num_summed_rows != 15:
            discrepancies.append(f"Row count check FAILED: '{input1}' has {num_summed_rows} rows, expected 15.")
        else:
            results.append(f"Row count check PASSED: '{input1}' has exactly 15 rows.")

        faasr_log("Validating all values in summed_output.csv are integers")
        all_integers = True
        for i, row in enumerate(summed_rows):
            if len(row) == 0:
                discrepancies.append(f"Row {i+1} in '{input1}' is empty.")
                all_integers = False
                continue
            try:
                int(row[0].strip())
            except ValueError:
                discrepancies.append(f"Row {i+1} in '{input1}' contains non-integer value: '{row[0]}'.")
                all_integers = False

        if all_integers and num_summed_rows > 0:
            results.append(f"Integer validation PASSED: All values in '{input1}' are valid whole integers with no header.")

        faasr_log("Performing element-wise addition validation")
        if a_rows and b_rows and summed_rows:
            min_len = min(len(a_rows), len(b_rows), len(summed_rows))
            addition_errors = []
            for i in range(min_len):
                try:
                    a_val = int(a_rows[i][0].strip())
                    b_val = int(b_rows[i][0].strip())
                    expected = a_val + b_val
                    actual = int(summed_rows[i][0].strip())
                    if actual != expected:
                        addition_errors.append(
                            f"Row {i+1}: {input2}={a_val}, {input3}={b_val}, expected sum={expected}, got={actual}."
                        )
                except (ValueError, IndexError) as e:
                    addition_errors.append(f"Row {i+1}: Error during validation - {e}")

            if addition_errors:
                discrepancies.extend(addition_errors)
            else:
                results.append(f"Element-wise addition validation PASSED: All {min_len} rows match expected sums.")

            if len(a_rows) != len(b_rows):
                discrepancies.append(f"Row count mismatch: '{input2}' has {len(a_rows)} rows, '{input3}' has {len(b_rows)} rows.")
            if len(summed_rows) != len(a_rows):
                discrepancies.append(f"Row count mismatch: '{input1}' has {len(summed_rows)} rows, but input files have {len(a_rows)} rows.")

        faasr_log("Writing validation report")
        with open(report_path, 'w') as f:
            f.write("=== Validation Report for 'summed_output.csv' ===\n\n")
            if results:
                f.write("PASSED CHECKS:\n")
                for r in results:
                    f.write(f"  - {r}\n")
                f.write("\n")
            if discrepancies:
                f.write("DISCREPANCIES FOUND:\n")
                for d in discrepancies:
                    f.write(f"  - {d}\n")
            else:
                f.write("No discrepancies found. All validations passed.\n")

        faasr_log(f"Uploading validation report '{output1}' to S3 folder '{folder}'")
        try:
            faasr_put_file(local_file=output1, remote_file=output1, local_folder=local_tmp, remote_folder=folder)
            faasr_log(f"Uploaded '{output1}' successfully.")
        except Exception as e:
            faasr_log(f"ERROR: Could not upload '{output1}': {e}")

        faasr_log(f"Validation report written and uploaded to '{folder}/{output1}'.")

    except Exception as e:
        faasr_log(f"ERROR in task_3: {e}")