from FaaSr_py.client.py_client_stubs import faasr_put_file, faasr_get_file
import os
import csv

def task_3(folder='tutorial', input1='summed_output.csv', output1='validation_report.txt'):
    os.makedirs(folder, exist_ok=True)
    input_path = os.path.join(folder, input1)
    output_path = os.path.join(folder, output1)
    discrepancies = []
    valid_rows = 0
    row_count = 0
    faasr_get_file(remote_folder=folder, remote_file='summed_output.csv', local_file='tutorial/summed_output.csv')
    try:
        with open(input_path, 'r', newline='') as f:
            content = f.read()
        lines = content.splitlines()
        row_count = len(lines)
        if row_count != 10:
            discrepancies.append(f'Row count error: expected 10 rows, found {row_count} rows.')
        for i, line in enumerate(lines, start=1):
            if line.endswith(','):
                discrepancies.append(f"Row {i}: trailing comma detected -> '{line}'")
                continue
            if line != line.strip():
                discrepancies.append(f"Row {i}: extra whitespace detected -> '{line}'")
                continue
            stripped = line.strip()
            if ',' in stripped:
                discrepancies.append(f"Row {i}: multiple columns detected -> '{stripped}'")
                continue
            try:
                value = int(stripped)
            except ValueError:
                discrepancies.append(f"Row {i}: value is not a plain integer -> '{stripped}'")
                continue
            if value < 2 or value > 200:
                discrepancies.append(f'Row {i}: value {value} is out of expected range [2, 200].')
                continue
            valid_rows += 1
    except FileNotFoundError:
        discrepancies.append(f"Input file '{input1}' not found in folder '{folder}'.")
    with open(output_path, 'w') as report:
        report.write("=== Validation Report for '{}' ===\n\n".format(input1))
        if not discrepancies and row_count == 10:
            report.write('Validation PASSED.\n')
            report.write(f'Total rows: {row_count}\n')
            report.write(f'Valid rows: {valid_rows}\n')
            report.write('All values are plain integers within the range [2, 200].\n')
            report.write('No header, no trailing commas, no extra whitespace detected.\n')
        else:
            report.write('Validation FAILED.\n')
            report.write(f'Total rows found: {row_count}\n')
            report.write(f'Valid rows: {valid_rows}\n')
            report.write(f'Number of discrepancies: {len(discrepancies)}\n\n')
            report.write('Discrepancies:\n')
            for d in discrepancies:
                report.write(f'  - {d}\n')
    faasr_put_file(local_file='tutorial/validation_report.txt', remote_folder=folder, remote_file='validation_report.txt')
    print(f"Validation complete. Report written to '{output_path}'.")