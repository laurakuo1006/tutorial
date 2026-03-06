from FaaSr_py.client.py_client_stubs import faasr_put_file, faasr_get_file
import os
import csv

def task_2(folder='tutorial', input1='integers_a.csv', input2='integers_b.csv', output1='summed_results.csv'):
    faasr_get_file(remote_folder=folder, remote_file='integers_a.csv', local_file='tutorial/integers_a.csv')
    faasr_get_file(remote_folder=folder, remote_file='integers_b.csv', local_file='tutorial/integers_b.csv')
    os.makedirs(folder, exist_ok=True)
    path_a = os.path.join(folder, input1)
    path_b = os.path.join(folder, input2)
    path_out = os.path.join(folder, output1)
    with open(path_a, newline='') as f:
        reader = csv.DictReader(f)
        rows_a = [int(row['value']) for row in reader]
    with open(path_b, newline='') as f:
        reader = csv.DictReader(f)
        rows_b = [int(row['value']) for row in reader]
    if len(rows_a) != len(rows_b):
        raise ValueError(f'Row count mismatch: integers_a.csv has {len(rows_a)} rows, integers_b.csv has {len(rows_b)} rows.')
    if len(rows_a) != 15:
        raise ValueError(f'Expected 15 data rows, but found {len(rows_a)} rows.')
    sums = [a + b for a, b in zip(rows_a, rows_b)]
    with open(path_out, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['sum'])
        for s in sums:
            writer.writerow([s])
    print(f'Written {len(sums)} summed rows to {path_out}')
    faasr_put_file(local_file='tutorial/summed_results.csv', remote_folder=folder, remote_file='summed_results.csv')