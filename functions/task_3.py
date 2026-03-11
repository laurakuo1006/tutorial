import os
import csv
from FaaSr_py.client.py_client_stubs import faasr_get_file, faasr_put_file, faasr_log

def task_3(folder="tutorial", input1="summed_results.csv", input2="integers_a.csv", input3="integers_b.csv", output1="validation_report.txt"):
    try:
        os.makedirs("/tmp", exist_ok=True)

        local_summed = "summed_results.csv"
        local_a = "integers_a.csv"
        local_b = "integers_b.csv"
        local_report = "validation_report.txt"

        faasr_log(f"Downloading input files from S3 folder '{folder}'")

        try:
            faasr_get_file(local_file=local_summed, remote_file=input1, local_folder="/tmp", remote_folder=folder)
            faasr_log(f"Downloaded '{input1}' successfully.")
        except Exception as e:
            faasr_log(f"ERROR: Could not download '{input1}': {e}")

        try:
            faasr_get_file(local_file=local_a, remote_file=input2, local_folder="/tmp", remote_folder=folder)
            faasr_log(f"Downloaded '{input2}' successfully.")
        except Exception as e:
            faasr_log(f"ERROR: Could not download '{input2}': {e}")

        try:
            faasr_get_file(local_file=local_b, remote_file=input3, local_folder="/tmp", remote_folder=folder)
            faasr_log(f"Downloaded '{input3}' successfully.")
        except Exception as e:
            faasr_log(f"ERROR: Could not download '{input3}': {e}")

        summed_path = os.path.join("/tmp", local_summed)
        integers_a_path = os.path.join("/tmp", local_a)
        integers_b_path = os.path.join("/tmp", local_b)
        report_path = os.path.join("/tmp", local_report)

        report_lines = []
        all_passed = True

        def read_csv_single_column(filepath):
            values = []
            with open(filepath, newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:
                        values.append(row[0].strip())
            return values

        # Read all three files
        try:
            summed_raw = read_csv_single_column(summed_path)
            report_lines.append(f"Successfully read '{input1}'.")
            faasr_log(f"Successfully read '{input1}'.")
        except Exception as e:
            report_lines.append(f"ERROR: Could not read '{input1}': {e}")
            faasr_log(f"ERROR: Could not read '{input1}': {e}")
            all_passed = False
            summed_raw = []

        try:
            a_raw = read_csv_single_column(integers_a_path)
            report_lines.append(f"Successfully read '{input2}'.")
            faasr_log(f"Successfully read '{input2}'.")
        except Exception as e:
            report_lines.append(f"ERROR: Could not read '{input2}': {e}")
            faasr_log(f"ERROR: Could not read '{input2}': {e}")
            all_passed = False
            a_raw = []

        try:
            b_raw = read_csv_single_column(integers_b_path)
            report_lines.append(f"Successfully read '{input3}'.")
            faasr_log(f"Successfully read '{input3}'.")
        except Exception as e:
            report_lines.append(f"ERROR: Could not read '{input3}': {e}")
            faasr_log(f"ERROR: Could not read '{input3}': {e}")
            all_passed = False
            b_raw = []

        # Check (1): summed_results.csv contains exactly 10 rows with no header row
        report_lines.append("\n--- Check 1: Row count and no header row ---")
        faasr_log("Running Check 1: Row count and no header row")
        if len(summed_raw) == 10:
            report_lines.append("PASS: 'summed_results.csv' contains exactly 10 rows.")
        else:
            report_lines.append(f"FAIL: 'summed_results.csv' contains {len(summed_raw)} rows (expected 10).")
            all_passed = False

        # Check for header (non-integer first row)
        if summed_raw:
            try:
                int(summed_raw[0])
                report_lines.append("PASS: No header row detected in 'summed_results.csv' (first row is an integer).")
            except ValueError:
                report_lines.append(f"FAIL: Header row detected in 'summed_results.csv' (first row value: '{summed_raw[0]}').")
                all_passed = False

        # Parse integer values
        def parse_ints(raw_list, name):
            parsed = []
            errors = []
            for i, val in enumerate(raw_list):
                try:
                    parsed.append(int(val))
                except ValueError:
                    errors.append(f"Row {i}: '{val}' is not an integer.")
                    parsed.append(None)
            return parsed, errors

        summed_vals, summed_errors = parse_ints(summed_raw, input1)
        a_vals, a_errors = parse_ints(a_raw, input2)
        b_vals, b_errors = parse_ints(b_raw, input3)

        # Check (2): Each row in summed_results.csv is an integer in range [2, 200]
        report_lines.append("\n--- Check 2: Values in summed_results.csv within range [2, 200] ---")
        faasr_log("Running Check 2: Value range validation")
        range_issues = []
        for i, val in enumerate(summed_vals):
            if val is None:
                range_issues.append(f"Row {i}: non-integer value '{summed_raw[i]}'.")
            elif not (2 <= val <= 200):
                range_issues.append(f"Row {i}: value {val} is out of range [2, 200].")
        if range_issues:
            report_lines.append("FAIL: Range check issues found:")
            report_lines.extend(f"  {issue}" for issue in range_issues)
            all_passed = False
        else:
            report_lines.append("PASS: All values in 'summed_results.csv' are within range [2, 200].")

        # Check (3) and (4): Cross-validate row-by-row sums and row order
        report_lines.append("\n--- Check 3 & 4: Row-level cross-validation and row order ---")
        faasr_log("Running Check 3 & 4: Cross-validation of row-level sums")
        cross_issues = []
        num_rows = min(len(summed_vals), len(a_vals), len(b_vals))
        for i in range(num_rows):
            sv = summed_vals[i]
            av = a_vals[i]
            bv = b_vals[i]
            if sv is None or av is None or bv is None:
                cross_issues.append(f"Row {i}: Cannot validate due to non-integer value(s).")
            elif sv != av + bv:
                cross_issues.append(f"Row {i}: summed={sv}, a={av}, b={bv}, expected sum={av + bv}. MISMATCH.")

        if len(summed_vals) != len(a_vals) or len(summed_vals) != len(b_vals):
            cross_issues.append(f"Row count mismatch: summed={len(summed_vals)}, a={len(a_vals)}, b={len(b_vals)}.")

        if cross_issues:
            report_lines.append("FAIL: Cross-validation issues found:")
            report_lines.extend(f"  {issue}" for issue in cross_issues)
            all_passed = False
        else:
            report_lines.append("PASS: All row-level sums match. Row order is consistent with source files.")

        # Summary
        report_lines.append("\n--- Summary ---")
        if all_passed:
            report_lines.append("ALL CHECKS PASSED. 'summed_results.csv' is valid.")
        else:
            report_lines.append("ONE OR MORE CHECKS FAILED. See details above.")

        faasr_log("Writing validation report to /tmp")
        with open(report_path, 'w') as f:
            f.write("\n".join(report_lines) + "\n")

        faasr_log(f"Uploading validation report '{output1}' to S3 folder '{folder}'")
        faasr_put_file(local_file=local_report, remote_file=output1, local_folder="/tmp", remote_folder=folder)
        faasr_log(f"Validation report '{output1}' successfully uploaded to S3.")

    except Exception as e:
        faasr_log(f"ERROR in task_3: {e}")
        raise