from FaaSr_py.client.py_client_stubs import faasr_put_file, faasr_get_file
import os
import sys
import csv

def task_3(folder='tutorial', input1='summed_output.csv'):
    faasr_get_file(remote_folder=folder, remote_file='summed_output.csv', local_file='tutorial/summed_output.csv')
    os.makedirs(folder, exist_ok=True)
    summed_output_path = os.path.join(folder, input1)
    with open(summed_output_path, newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    actual_count = len(rows)
    if actual_count != 10:
        print(f'ERROR: summed_output.csv contains {actual_count} data rows, expected 10.')
        sys.exit(1)
    verified_values = []
    for i, row in enumerate(rows, start=1):
        raw_value = row['sum']
        try:
            val = int(raw_value)
        except ValueError:
            print(f'ERROR: summed_output.csv contains an out-of-range or invalid value at row {i}: {raw_value}')
            sys.exit(1)
        if val < 2 or val > 200:
            print(f'ERROR: summed_output.csv contains an out-of-range or invalid value at row {i}: {val}')
            sys.exit(1)
        verified_values.append(val)
    print(f'Verified summed_output.csv values: {verified_values}')
    print('VERIFICATION PASSED: summed_output.csv contains 10 valid integer sum values in the expected range 2-200.')