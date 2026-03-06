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
        rows_a = [row for row in reader]
    with open(path_b, newline='') as f:
        reader = csv.DictReader(f)
        rows_b = [row for row in reader]
    assert len(rows_a) == 10, f'Expected 10 rows in {input1}, got {len(rows_a)}'
    assert len(rows_b) == 10, f'Expected 10 rows in {input2}, got {len(rows_b)}'
    header_a = list(rows_a[0].keys())[0]
    header_b = list(rows_b[0].keys())[0]
    sums = []
    for row_a, row_b in zip(rows_a, rows_b):
        val_a = int(row_a[header_a])
        val_b = int(row_b[header_b])
        sums.append(val_a + val_b)
    with open(path_out, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['sum'])
        for s in sums:
            writer.writerow([s])
    print(f'Written {len(sums)} summed rows to {path_out}')
    faasr_put_file(local_file='tutorial/summed_results.csv', remote_folder=folder, remote_file='summed_results.csv')